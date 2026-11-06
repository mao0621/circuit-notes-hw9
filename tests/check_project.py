"""Offline acceptance tests. Run from any directory: python tests/check_project.py.

All builds and extension experiments run in disposable copies; source lesson files
are never edited by the tests. No third-party Python packages are required.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("circuit_builder", ROOT / "build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.attrs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.attrs.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])

    handle_startendtag = handle_starttag


def clone_project(destination):
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", ".pytest_cache", "docs", "*.ipynb", "*.zip"
    ))
    return destination


def run_build(project):
    result = subprocess.run([sys.executable, "build.py"], cwd=project,
                            encoding="utf-8", capture_output=True)
    if result.returncode:
        raise AssertionError("Build failed:\n" + result.stdout + result.stderr)
    return result.stdout


def digest_tree(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file()}


class ProjectChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="circuit-notes-check-", dir=ROOT.parent)
        cls.project = clone_project(Path(cls.temp.name) / "project")
        cls.lessons = builder.load_lessons()
        run_build(cls.project)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_01_schema_and_expected_content(self):
        self.assertGreaterEqual(len(self.lessons), 3)
        self.assertEqual(len({d["slug"] for d in self.lessons}), len(self.lessons))
        self.assertTrue({"ohms-law", "voltage-divider", "rc-time-constant"}
                        <= {d["slug"] for d in self.lessons})
        template = json.loads((ROOT / "content/template.json").read_text(encoding="utf-8"))
        self.assertEqual(set(template), builder.REQUIRED)
        self.assertNotIn(template["slug"], {d["slug"] for d in self.lessons})

    def test_02_invalid_content_is_rejected(self):
        sample = self.lessons[0]
        mutations = {
            "invalid slug": lambda x: x.update(slug="../escape"),
            "unknown field": lambda x: x.update(unexpected="ignored?"),
            "missing field": lambda x: x.pop("summary"),
            "empty sources": lambda x: x.update(sources=[]),
            "script URL": lambda x: x.update(sources=[{"label": "bad", "url": "javascript:alert(1)"}]),
            "wrong difficulty": lambda x: x.update(difficulty="unknown"),
            "boolean reading time": lambda x: x.update(minutes=True),
            "unknown lab": lambda x: x.update(lab="unknown"),
            "empty sections": lambda x: x.update(sections=[]),
            "empty exercise": lambda x: x.update(exercise={}),
        }
        for label, mutate in mutations.items():
            with self.subTest(case=label):
                data = copy.deepcopy(sample)
                mutate(data)
                with self.assertRaises(ValueError):
                    builder.validate_lesson(data, Path(sample["slug"] + ".json"))

    def test_03_filenames_and_orders_are_checked(self):
        with self.assertRaises(ValueError):
            builder.validate_lesson(copy.deepcopy(self.lessons[0]), Path("wrong-name.json"))
        with tempfile.TemporaryDirectory(prefix="circuit-schema-", dir=ROOT.parent) as temp:
            directory = Path(temp)
            a, b = copy.deepcopy(self.lessons[:2])
            b["order"] = a["order"]
            for data in (a, b):
                (directory / (data["slug"] + ".json")).write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate order"):
                builder.load_lessons(directory)

    def test_04_html_content_is_escaped(self):
        attack = '<script>alert("lesson")</script>&'
        sample = copy.deepcopy(self.lessons[0])
        sample["title"] = attack
        sample["summary"] = attack
        sample["sections"][0]["paragraphs"] = [attack]
        sample["sections"][0]["formula"] = attack
        sample["exercise"]["answer"] = attack
        sample["sources"][0]["label"] = attack
        rendered = builder.shell(attack, builder.lesson_body(sample, [sample]), [sample])
        self.assertNotIn(attack, rendered)
        self.assertIn("&lt;script&gt;", rendered)
        parsed = Page(rendered)
        self.assertEqual([attrs.get("src") for tag, attrs in parsed.attrs if tag == "script"],
                         ["assets/app.js"])

    def test_05_internal_paths_and_anchors(self):
        out = self.project / "docs"
        pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in out.rglob("*.html")}
        self.assertGreaterEqual(len(pages), 6)
        for file, page in pages.items():
            with self.subTest(page=file.name):
                self.assertEqual(len(page.ids), len(set(page.ids)), "duplicate IDs")
            for link in page.links:
                with self.subTest(page=file.name, link=link):
                    url = urlsplit(link)
                    if url.scheme or url.netloc:
                        continue
                    self.assertFalse(url.path.startswith("/"), "project Pages paths must be relative")
                    target = (file.parent / unquote(url.path)).resolve() if url.path else file
                    self.assertTrue(target.is_relative_to(out.resolve()), "link escapes docs directory")
                    self.assertTrue(target.is_file(), "internal file missing")
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), pages[target].ids, "anchor missing")

    def test_06_rules_copy_matches_source(self):
        out = self.project / "docs"
        rules = (self.project / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual((out / "AGENTS.md").read_text(encoding="utf-8"), rules)
        self.assertIn(builder.e(rules), (out / "rules.html").read_text(encoding="utf-8"))
        self.assertTrue((out / ".nojekyll").is_file())

    def test_07_build_is_reproducible(self):
        before = digest_tree(self.project / "docs")
        run_build(self.project)
        self.assertEqual(before, digest_tree(self.project / "docs"))

    def test_08_extend_two_lessons_to_three(self):
        with tempfile.TemporaryDirectory(prefix="circuit-extend-", dir=ROOT.parent) as temp:
            project = clone_project(Path(temp) / "project")
            lesson = project / "content/lessons/rc-time-constant.json"
            saved = lesson.read_bytes()
            lesson.unlink()  # Only disposable test copy; main project is untouched.
            core_before = {name: (project / name).read_bytes() for name in
                           ("build.py", "assets/app.js", "assets/styles.css")}
            run_build(project)
            out = project / "docs"
            self.assertEqual(len(list((out / "lessons").glob("*.html"))), 2)
            self.assertNotIn('data-slug="rc-time-constant"', (out / "index.html").read_text(encoding="utf-8"))
            lesson.write_bytes(saved)
            run_build(project)
            self.assertEqual(len(list((out / "lessons").glob("*.html"))), 3)
            self.assertIn('data-slug="rc-time-constant"', (out / "index.html").read_text(encoding="utf-8"))
            self.assertIn('href="../lessons/rc-time-constant.html"',
                          (out / "lessons/ohms-law.html").read_text(encoding="utf-8"))
            for name, contents in core_before.items():
                self.assertEqual(contents, (project / name).read_bytes(), "extension modified core")

    def test_09_add_fourth_lesson_without_core_changes(self):
        with tempfile.TemporaryDirectory(prefix="circuit-fourth-", dir=ROOT.parent) as temp:
            project = clone_project(Path(temp) / "project")
            data = json.loads((project / "content/template.json").read_text(encoding="utf-8"))
            data.update(slug="series-resistors-test", title="串聯電阻測試課文", lab="none",
                        order=max(d["order"] for d in self.lessons) + 1,
                        category="延伸測試", difficulty="進階")
            (project / "content/lessons/series-resistors-test.json").write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            core_before = {name: (project / name).read_bytes() for name in
                           ("build.py", "assets/app.js", "assets/styles.css")}
            run_build(project)
            index = (project / "docs/index.html").read_text(encoding="utf-8")
            page = (project / "docs/lessons/series-resistors-test.html").read_text(encoding="utf-8")
            self.assertIn('data-slug="series-resistors-test"', index)
            self.assertIn('<option>延伸測試</option>', index)
            self.assertIn('href="../lessons/series-resistors-test.html"', page)
            self.assertIn("串聯電阻測試課文", page)
            self.assertNotIn('data-lab=', page)
            self.assertNotIn('href="#lab"', page)
            for name, contents in core_before.items():
                self.assertEqual(contents, (project / name).read_bytes(), "extension modified core")

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable; browser math check still required")
    def test_10_javascript_calculations_and_boundaries(self):
        script = r'''
const assert = require('node:assert/strict');
const m = require(process.argv[1]);
const close = (a, b, tolerance = 1e-9) => assert.ok(Math.abs(a-b) <= tolerance, `${a} != ${b}`);
const ohm = m.ohm(5, 1000); close(ohm.currentMA, 5); close(ohm.powerMW, 25);
const divider = m.divider(9, 20000, 10000, 10000);
close(divider.unloaded, 3); close(divider.loaded, 1.8); close(divider.dropPercent, 40);
const rc = m.rc(20, 50, 1); close(rc.tau, 1); close(rc.time, 1); close(rc.voltage, 3.1606027941427883);
close(m.ohm(0, 1000).currentMA, 0); close(m.divider(0, 1000, 1000, 1000).loaded, 0);
close(m.rc(20, 50, 0).voltage, 0); close(m.rc(20, 50, 5).percent, 99.32620530009146);
for (const [name, args] of [
  ['ohm', [5, 0]], ['ohm', [-1, 1000]], ['ohm', [NaN, 1000]], ['ohm', [5, Infinity]],
  ['divider', [5, 1000, 0, 1000]], ['divider', [5, -1, 1000, 1000]],
  ['divider', [NaN, 1000, 1000, 1000]], ['divider', [5, 1000, 1000, Infinity]],
  ['rc', [0, 100, 1]], ['rc', [10, -100, 1]], ['rc', [10, 100, -1]], ['rc', [10, 100, NaN]],
]) assert.equal(m[name](...args), null, `${name}: invalid input must return null`);
console.log('Reference values and boundary checks passed.');
'''
        result = subprocess.run([shutil.which("node"), "-e", script, str(ROOT / "assets/app.js")],
                                encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

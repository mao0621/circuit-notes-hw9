"""Build Circuit Notes with Python's standard library. Run: python build.py"""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
REQUIRED = {"slug", "title", "summary", "category", "difficulty", "minutes", "order", "tags", "objectives", "sections", "pitfalls", "exercise", "lab", "sources"}


def e(value):
    return html.escape(str(value), quote=True)


def validate_lesson(data, path):
    """Reject malformed content early rather than silently publish an empty page."""
    def require(condition, message):
        if not condition:
            raise ValueError(f"{path.name}: {message}")

    require(isinstance(data, dict), "lesson must be an object")
    require(set(data) == REQUIRED, f"fields must match schema; missing={REQUIRED - set(data)}, extra={set(data) - REQUIRED}")
    require(isinstance(data["slug"], str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["slug"]), "invalid kebab-case slug")
    require(path.stem == data["slug"], "filename must match slug")
    for key in ("title", "summary", "category", "difficulty"):
        require(isinstance(data[key], str) and bool(data[key].strip()), f"{key} must be nonempty text")
    require(data["difficulty"] in ("入門", "進階"), "difficulty must be 入門 or 進階")
    for key in ("minutes", "order"):
        require(type(data[key]) is int and data[key] > 0, f"{key} must be a positive integer")
    for key in ("tags", "objectives", "pitfalls"):
        require(isinstance(data[key], list) and len(data[key]) > 0 and all(isinstance(x, str) and x.strip() for x in data[key]), f"{key} must be a nonempty list of text")
    require(data["lab"] in ("ohm", "divider", "rc", "none"), "unknown lab")
    require(isinstance(data["sections"], list) and len(data["sections"]) >= 3, "at least three sections are required")
    for section in data["sections"]:
        require(isinstance(section, dict) and {"heading", "paragraphs"} <= set(section) <= {"heading", "paragraphs", "formula"}, "section fields are heading, paragraphs, optional formula")
        require(isinstance(section["heading"], str) and section["heading"].strip(), "section heading is required")
        require(isinstance(section["paragraphs"], list) and section["paragraphs"] and all(isinstance(x, str) and x.strip() for x in section["paragraphs"]), "section paragraphs must contain text")
        if "formula" in section:
            require(isinstance(section["formula"], str) and section["formula"].strip(), "formula must be text")
    require(isinstance(data["exercise"], dict) and set(data["exercise"]) == {"question", "hint", "answer"}, "exercise fields are question, hint, answer")
    require(all(isinstance(x, str) and x.strip() for x in data["exercise"].values()), "exercise text cannot be empty")
    require(isinstance(data["sources"], list) and data["sources"], "source required")
    for source in data["sources"]:
        require(isinstance(source, dict) and set(source) == {"label", "url"}, "source fields are label, url")
        require(isinstance(source["label"], str) and source["label"].strip(), "source label required")
        require(isinstance(source["url"], str) and urlparse(source["url"]).scheme == "https" and urlparse(source["url"]).netloc, "source must use an absolute HTTPS URL")
    return data


def load_lessons(directory=None):
    files = sorted((directory or ROOT / "content" / "lessons").glob("*.json"))
    if not files:
        raise ValueError("content/lessons must contain at least one lesson")
    lessons = [validate_lesson(json.loads(p.read_text(encoding="utf-8")), p) for p in files]
    for key in ("slug", "order"):
        values = [d[key] for d in lessons]
        if len(set(values)) != len(values):
            raise ValueError(f"duplicate {key}")
    return sorted(lessons, key=lambda d: d["order"])


def circuit_svg(kind="ohm"):
    """Small original vector diagram; all labels are readable text."""
    if kind == "divider":
        return '<svg viewBox="0 0 320 180" role="img" aria-label="上方R₁與下方R₂串聯，輸出取中間節點的分壓器"><path d="M75 28h85v12l-10 6 20 10-20 10 10 6v16m0 0v10l-10 6 20 10-20 10 10 6v30m0-72h75m-90 72h30m-24 6h18m-12 6h6"/><text x="186" y="60">R₁</text><text x="186" y="124">R₂</text><text x="22" y="32">Vin</text><text x="240" y="92">Vout</text><circle cx="75" cy="28" r="3" class="node"/><circle cx="160" cy="88" r="4" class="node"/></svg>'
    if kind == "rc":
        return '<svg viewBox="0 0 320 180" role="img" aria-label="串聯電阻與電容的RC充電電路"><path d="M42 130V58h48l8-12 12 24 12-24 12 24 8-12h80v28m-22 0h44m-44 13h44m-22 0v31H42"/><text x="105" y="32">R</text><text x="255" y="98">C</text><text x="63" y="158">τ = RC</text><circle cx="222" cy="58" r="4" class="node"/></svg>'
    return '<svg viewBox="0 0 320 180" role="img" aria-label="電壓源與電阻串聯的歐姆定律電路"><path d="M65 65V40h70l8-12 12 24 12-24 12 24 8-12h70v100H65v-25"/><circle cx="65" cy="90" r="25"/><path d="M55 82h20m-10-10v20m-10 10h20"/><path d="M209 140h-38m7-6-7 6 7 6"/><text x="28" y="94">V</text><text x="148" y="20">R</text><text x="185" y="166">I</text><circle cx="257" cy="40" r="4" class="node"/></svg>'


def shell(title, body, lessons, prefix="", active="home", description="用一致的規則，整理可持續擴充的電路學習筆記。"):
    nav_parts = []
    for i, d in enumerate(lessons, 1):
        css_active = 'active' if active == d['slug'] else ''
        current = 'aria-current="page"' if css_active else ''
        nav_parts.append(f'<a href="{prefix}lessons/{e(d["slug"])}.html" class="lesson-nav {css_active}" {current}><span>{i:02}</span>{e(d["title"])}</a>')
    nav = ''.join(nav_parts)
    home_current = 'aria-current="page"' if active == 'home' else ''
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}｜Circuit Notes 電路筆記工坊</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#173d35"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/styles.css"><script defer src="{prefix}assets/app.js"></script></head>
<body><a class="skip-link" href="#main">跳至主要內容</a>
<aside class="sidebar"><a class="brand" href="{prefix}index.html" aria-label="Circuit Notes 首頁"><span class="brand-symbol">C<span>＋</span></span><span>Circuit Notes<small>電路筆記工坊</small></span></a>
<span class="nav-label">WORKSPACE / 學習空間</span><nav aria-label="主要導覽"><a class="nav-main {"active" if active == "home" else ""}" href="{prefix}index.html" {home_current}><span aria-hidden="true">▦</span>所有筆記<span class="count">{len(lessons)}</span></a><a class="nav-main {"active" if active == "rules" else ""}" href="{prefix}rules.html"><span aria-hidden="true">⌘</span>專案規則<span class="tiny">MD</span></a></nav>
<span class="nav-label notes-label">NOTEBOOK / 電路觀念</span><nav aria-label="課文導覽">{nav}</nav>
<div class="sidebar-bottom"><span class="status-dot"></span>小觀念，慢慢接起來。<p>從一條公式，到一套能持續<br>累積的學習筆記。</p><span class="edition">GEN AI · WEEK 09</span></div></aside>
<div class="workspace"><header class="topbar"><span>學習工作台 <b>/</b> {e(title)}</span><a href="{prefix}rules.html" class="rules-pill"><i></i>依 AGENTS.md 建立</a></header>
<main id="main">{body}</main><footer><span>電路筆記工坊 <b>·</b> 把規則留下，讓知識繼續長大。</span><a href="{prefix}AGENTS.md">閱讀 AGENTS.md ↗</a></footer></div>
</body></html>'''


def home(lessons):
    cards = []
    for i, d in enumerate(lessons, 1):
        search = " ".join([d["title"], d["summary"], d["category"], *d["tags"]])
        cards.append(f'''<article class="note-card" data-search="{e(search)}" data-category="{e(d['category'])}" data-difficulty="{e(d['difficulty'])}" data-slug="{e(d['slug'])}">
<div class="card-head"><span class="note-number">NOTE {i:02}</span><button class="bookmark" data-bookmark="{e(d['slug'])}" aria-label="收藏：{e(d['title'])}" aria-pressed="false"><span aria-hidden="true">☆</span></button></div>
<a class="diagram-link" href="lessons/{e(d['slug'])}.html" aria-label="閱讀{e(d['title'])}">{circuit_svg(d['lab'])}</a>
<div class="card-body"><span class="eyebrow">{e(d['category'])} <b>·</b> {e(d['difficulty'])}</span><h3><a href="lessons/{e(d['slug'])}.html">{e(d['title'])}</a></h3><p>{e(d['summary'])}</p><div class="tags">{''.join(f'<span>#{e(t)}</span>' for t in d['tags'])}</div></div>
<a class="card-bottom" href="lessons/{e(d['slug'])}.html"><span>約 {d['minutes']} 分鐘 <b>·</b> 含練習</span><span>開始閱讀 ↗</span></a></article>''')
    categories = sorted({d["category"] for d in lessons})
    category_options = ''.join(f'<option>{e(c)}</option>' for c in categories)
    return f'''<section class="hero"><div class="hero-copy"><span class="kicker"><i></i> A NOTEBOOK THAT GROWS WITH YOU</span><h1>把電路觀念，<br>接成自己的<span>知識。</span></h1><p>整理公式、拆解觀念，再動手試一次。<br>用一套共同規則，讓每篇筆記都能接著寫下去。</p><a href="#notebook" class="primary-button">打開我的筆記 <span>↘</span></a><div class="hero-meta"><span>{len(lessons):02} 篇主題筆記</span><i></i><span>{sum(d['lab'] != 'none' for d in lessons):02} 個互動實驗</span><i></i><span>01 套內容規則</span></div></div>
<div class="hero-board"><div class="board-top"><span>THE EVERYDAY CIRCUIT</span><span>FIG. 01</span></div>{circuit_svg()}<div class="formula-sticker"><small>從這裡開始</small><strong>V = I × R</strong><span>一條公式，連起三個觀念。</span></div><span class="board-caption">先理解，再計算，最後驗證。</span><div class="board-plus" aria-hidden="true">＋</div></div></section>
<section id="notebook" class="notebook-section"><div class="section-title"><div><span class="eyebrow">MY NOTEBOOK</span><h2>今天想弄懂哪個觀念？</h2></div><span id="result-count" class="result-count" role="status">共 {len(lessons)} 篇筆記</span></div>
<div class="filters"><label class="search-field"><span aria-hidden="true">⌕</span><input id="search" type="search" aria-label="搜尋筆記" placeholder="搜尋觀念、公式或關鍵字…"></label><label class="select-field"><span class="sr-only">分類</span><select id="category"><option value="">所有分類</option>{category_options}</select></label><label class="select-field"><span class="sr-only">難度</span><select id="difficulty"><option value="">所有難度</option><option>入門</option><option>進階</option></select></label><label class="saved-filter"><input id="saved-only" type="checkbox">只看收藏</label></div>
<div class="note-grid">{''.join(cards)}</div><div id="empty-state" class="empty-state" hidden><strong>還沒有符合的筆記</strong><p>試試其他關鍵字，或取消「只看收藏」。</p><button id="reset-filters" class="text-button">清除所有篩選 ↺</button></div><p id="storage-note" class="storage-note">收藏儲存在目前瀏覽器中。</p></section>
<section class="extension-banner"><span class="extension-icon" aria-hidden="true">↳</span><div><span class="eyebrow">BUILT TO CONTINUE</span><h2>下一篇筆記，從規則開始。</h2><p>複製內容範本、補齊觀念與練習，再重新建置。<br>導覽、卡片和課文頁面會沿用同一套格式。</p></div><a href="rules.html" class="secondary-button">看看這套規則 ↗</a></section>'''


def lab_html(kind):
    if kind == "none":
        return ""
    sliders = {
        "ohm": [('voltage', '電壓 V', 0, 12, 5, 0.1, 'V'), ('resistance', '電阻 R', 100, 10000, 1000, 100, 'Ω')],
        "divider": [('vin', '輸入電壓 Vin', 0, 12, 5, 0.1, 'V'), ('r1', '上方電阻 R₁', 100, 10000, 1000, 100, 'Ω'), ('r2', '下方電阻 R₂', 100, 10000, 2000, 100, 'Ω'), ('load', '負載電阻 Rᴸ', 100, 50000, 10000, 100, 'Ω')],
        "rc": [('rc-r', '電阻 R', 1, 100, 10, 1, 'kΩ'), ('rc-c', '電容 C', 1, 1000, 100, 1, 'μF'), ('time', '經過時間 t / τ', 0, 5, 1, 0.1, 'τ')]
    }
    controls = ''.join(f'<label class="range-label" for="{key}"><span>{label}</span><output id="{key}-value" for="{key}">{value} {unit}</output></label><input type="range" id="{key}" min="{low}" max="{high}" value="{value}" step="{step}" data-unit="{unit}">' for key, label, low, high, value, step, unit in sliders[kind])
    disclaimer = {'ohm':'模型假設：理想直流電壓源與固定阻值的歐姆電阻。','divider':'模型假設：電阻為理想元件，負載與 R₂ 並聯。','rc':'模型假設：初始電壓為 0、理想電容充電，輸入電壓階躍為 5 V。'}[kind]
    chart = '<svg id="rc-chart" viewBox="0 0 480 200" role="img" aria-label="RC充電曲線：橫軸為時間除以時間常數，縱軸為電容電壓"><path class="chart-grid" d="M42 20v145h410M42 92h410M124 20v145M206 20v145M288 20v145M370 20v145M452 20v145"/><path id="rc-curve" class="chart-curve"/><circle id="rc-point" r="5"/><text x="6" y="25">5 V</text><text x="15" y="170">0</text><text x="110" y="188">1τ</text><text x="430" y="188">5τ</text></svg>' if kind == "rc" else ''
    return f'<section id="lab" class="lesson-section lab" data-lab="{kind}"><span class="eyebrow">TRY IT YOURSELF</span><h2>互動實驗室</h2><p>移動滑桿，觀察數值之間的關係。</p><div class="lab-layout"><div class="lab-controls">{controls}</div><div class="lab-result" id="lab-result" role="status" aria-live="polite"></div></div>{chart}<small class="model-note">{disclaimer}</small></section>'


def lesson_body(d, lessons):
    index = lessons.index(d)
    section_parts = []
    for i, s in enumerate(d['sections'], 1):
        paragraphs = ''.join('<p>' + e(p) + '</p>' for p in s['paragraphs'])
        formula = '<div class="formula-box">' + e(s['formula']) + '</div>' if 'formula' in s else ''
        section_parts.append(f'<section class="lesson-section" id="section-{i}"><span class="section-index">{i:02}</span><h2>{e(s["heading"])}</h2>{paragraphs}{formula}</section>')
    sections = ''.join(section_parts)
    toc = ''.join(f'<a href="#section-{i}">{i:02} {e(s["heading"])}</a>' for i, s in enumerate(d['sections'], 1))
    sources = ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])} ↗</a></li>' for s in d['sources'])
    next_d = lessons[(index+1) % len(lessons)]
    return f'''<div class="lesson-heading"><a href="../index.html" class="back-link">← 所有筆記</a><div class="lesson-heading-meta"><span class="eyebrow">NOTE {index+1:02} / {e(d['category'])}</span><button class="bookmark" data-bookmark="{e(d['slug'])}" aria-label="收藏：{e(d['title'])}" aria-pressed="false"><span aria-hidden="true">☆</span></button></div><h1>{e(d['title'])}</h1><p>{e(d['summary'])}</p><div class="lesson-meta"><span>{e(d['difficulty'])}</span><span>約 {d['minutes']} 分鐘</span>{''.join(f'<span>#{e(t)}</span>' for t in d['tags'])}</div></div>
<div class="reading-layout"><article class="lesson-content"><section class="objectives"><span class="eyebrow">AFTER THIS NOTE</span><h2>讀完這篇，你可以…</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in d['objectives'])}</ul></section>{sections}{lab_html(d['lab'])}<section id="pitfalls" class="lesson-section pitfalls"><span class="eyebrow">PAY ATTENTION</span><h2>容易接錯的觀念</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in d['pitfalls'])}</ul></section>
<section id="exercise" class="lesson-section exercise"><span class="eyebrow">ONE SMALL CHALLENGE</span><h2>換你算算看</h2><p>{e(d['exercise']['question'])}</p><p class="hint">提示：{e(d['exercise']['hint'])}</p><details><summary>展開解題步驟</summary><p>{e(d['exercise']['answer'])}</p></details></section><section id="sources" class="lesson-section sources"><h2>延伸閱讀與資料來源</h2><ul>{sources}</ul></section><a class="next-note" href="{e(next_d['slug'])}.html"><span>接著看看下一個觀念</span><strong>{e(next_d['title'])} ↗</strong></a></article><aside class="toc" aria-label="本篇目錄"><span class="eyebrow">IN THIS NOTE</span>{toc}{'<a href="#lab">互動實驗室</a>' if d['lab'] != 'none' else ''}<a href="#pitfalls">易錯觀念</a><a href="#exercise">小練習</a><a href="#sources">資料來源</a></aside></div>'''


def rules_body(rules, lessons):
    rc_link = '<a class="secondary-button" href="lessons/rc-time-constant.html">打開 RC 筆記 ↗</a>' if any(d['slug'] == 'rc-time-constant' for d in lessons) else '<a class="secondary-button" href="index.html">瀏覽現有筆記 ↗</a>'
    return f'''<section class="rules-heading"><span class="kicker">ONE GUIDE, MANY NOTES</span><h1>寫下一篇之前，<br>先讀懂這套規則。</h1><p>AGENTS.md 是這個專案的共同約定：讓 AI 知道內容放哪裡、該怎麼寫，以及完成後如何驗證。</p></section><section class="workflow"><div><span>01</span><h2>讀取規則</h2><p>先看目的、欄位與修改範圍。</p></div><div><span>02</span><h2>複製範本</h2><p>新增一份課文 JSON，補齊觀念。</p></div><div><span>03</span><h2>建置與檢查</h2><p>確認格式、計算與所有連結。</p></div><div><span>04</span><h2>持續延伸</h2><p>沿用版面，新增有來源的筆記。</p></div></section><section class="rules-document"><div class="code-toolbar"><span>AGENTS.md <small>· 專案根目錄</small></span><div><button id="copy-rules" class="text-button">複製規則</button><a href="AGENTS.md" download>下載 ↧</a></div></div><pre id="rules-text">{e(rules)}</pre><p id="copy-status" class="sr-only" role="status"></p></section><section class="extension-banner"><span class="extension-icon" aria-hidden="true">＋</span><div><span class="eyebrow">EXTENSION EXAMPLE</span><h2>用 RC 筆記，示範規則延伸。</h2><p>沿用相同欄位新增 rc-time-constant.json。<br>建置程式會自動加入首頁、導覽與獨立課文頁。</p></div>{rc_link}</section>'''


def build():
    lessons = load_lessons()
    rules = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    (OUT / 'lessons').mkdir(parents=True, exist_ok=True)
    (OUT / 'assets').mkdir(parents=True, exist_ok=True)
    valid_pages = {d['slug'] + '.html' for d in lessons}
    # Only remove stale generated lesson files after checking their resolved directory.
    for old in (OUT / 'lessons').glob('*.html'):
        if old.name not in valid_pages and old.resolve().parent == (OUT / 'lessons').resolve():
            old.unlink()
    for name in ('styles.css', 'app.js', 'favicon.svg'):
        shutil.copyfile(ROOT / 'assets' / name, OUT / 'assets' / name)
    (OUT / 'index.html').write_text(shell('所有筆記', home(lessons), lessons), encoding='utf-8')
    for d in lessons:
        (OUT / 'lessons' / f"{d['slug']}.html").write_text(shell(d['title'], lesson_body(d, lessons), lessons, prefix='../', active=d['slug'], description=d['summary']), encoding='utf-8')
    (OUT / 'rules.html').write_text(shell('專案規則', rules_body(rules, lessons), lessons, active='rules'), encoding='utf-8')
    (OUT / 'AGENTS.md').write_text(rules, encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    # No root-relative assets: GitHub project sites may live under /repository/.
    # 404 is self-contained because the missing URL's nesting depth is unknown.
    (OUT / '404.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>找不到這篇筆記</title><style>body{font:18px system-ui;background:#f7f6f0;color:#173d35;max-width:40rem;margin:15vh auto;padding:2rem}button{font:inherit;padding:.8rem;cursor:pointer}</style><h1>這條線還沒接上。</h1><p>找不到這篇筆記，請從網站首頁重新選擇。</p><button onclick="history.back()">← 回到上一頁</button></html>', encoding='utf-8')
    print(f'Built {len(lessons)} lessons, index, rules and 404 → docs/')


if __name__ == '__main__':
    build()

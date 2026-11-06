"use strict";

// Pure calculations share the exact same units as the displayed controls.
const CircuitMath = Object.freeze({
  ohm(voltage, resistance) {
    if (!Number.isFinite(voltage) || voltage < 0 || !Number.isFinite(resistance) || resistance <= 0) return null;
    return { currentMA: voltage / resistance * 1000, powerMW: voltage ** 2 / resistance * 1000 };
  },
  divider(vin, r1, r2, load) {
    if (![vin, r1, r2, load].every(Number.isFinite) || vin < 0 || Math.min(r1, r2, load) <= 0) return null;
    const parallel = r2 * load / (r2 + load);
    const unloaded = vin * r2 / (r1 + r2);
    const loaded = vin * parallel / (r1 + parallel);
    return { parallel, unloaded, loaded, dropPercent: unloaded > 0 ? (1 - loaded / unloaded) * 100 : 0 };
  },
  rc(rKOhm, cMicroF, multiples) {
    if (![rKOhm, cMicroF, multiples].every(Number.isFinite) || Math.min(rKOhm, cMicroF) <= 0 || multiples < 0) return null;
    const tau = rKOhm * 1000 * cMicroF * 1e-6;
    const fraction = 1 - Math.exp(-multiples);
    return { tau, time: tau * multiples, voltage: 5 * fraction, percent: 100 * fraction };
  }
});
if (typeof module !== "undefined" && module.exports) module.exports = CircuitMath;

if (typeof document !== "undefined") {
  const $ = (id) => document.getElementById(id);
  const key = "circuit-notes:bookmarks:v1";
  let saved = new Set();
  let storageAvailable = true;
  try {
    const parsed = JSON.parse(localStorage.getItem(key) || "[]");
    if (Array.isArray(parsed)) saved = new Set(parsed.filter((x) => typeof x === "string"));
  } catch (_) { storageAvailable = false; }

  function storageNote() {
    if ($("storage-note") && !storageAvailable) $("storage-note").textContent = "此瀏覽器無法保存收藏；本次開啟期間仍可收藏與篩選。";
  }
  function paintBookmarks() {
    document.querySelectorAll("[data-bookmark]").forEach((button) => {
      const marked = saved.has(button.dataset.bookmark);
      button.setAttribute("aria-pressed", String(marked));
      button.querySelector("span").textContent = marked ? "★" : "☆";
    });
  }
  function filterNotes() {
    if (!$("search")) return;
    const query = $("search").value.trim().toLocaleLowerCase();
    const tokens = query.split(/\s+/).filter(Boolean);
    let visible = 0;
    document.querySelectorAll(".note-card").forEach((card) => {
      const matches = tokens.every((token) => card.dataset.search.toLocaleLowerCase().includes(token))
        && (!$("category").value || card.dataset.category === $("category").value)
        && (!$("difficulty").value || card.dataset.difficulty === $("difficulty").value)
        && (!$("saved-only").checked || saved.has(card.dataset.slug));
      card.hidden = !matches;
      if (matches) visible++;
    });
    $("result-count").textContent = `共 ${visible} 篇筆記`;
    $("empty-state").hidden = visible > 0;
  }
  document.querySelectorAll("[data-bookmark]").forEach((button) => {
    button.addEventListener("click", () => {
      const slug = button.dataset.bookmark;
      saved.has(slug) ? saved.delete(slug) : saved.add(slug);
      try { localStorage.setItem(key, JSON.stringify([...saved])); }
      catch (_) { storageAvailable = false; storageNote(); }
      paintBookmarks(); filterNotes();
    });
  });
  if ($("search")) {
    $("search").addEventListener("input", filterNotes);
    ["category", "difficulty", "saved-only"].forEach((id) => $(id).addEventListener("change", filterNotes));
    $("reset-filters").addEventListener("click", () => {
      $("search").value = ""; $("category").value = ""; $("difficulty").value = ""; $("saved-only").checked = false;
      filterNotes(); $("search").focus();
    });
    filterNotes();
  }
  paintBookmarks(); storageNote();

  if ($("copy-rules")) {
    $("copy-rules").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText($("rules-text").textContent);
        $("copy-rules").textContent = "已複製 ✓";
        $("copy-status").textContent = "已複製 AGENTS.md";
      } catch (_) {
        $("copy-rules").textContent = "請下載規則檔";
        $("copy-status").textContent = "瀏覽器無法複製，請使用旁邊的下載連結。";
      }
    });
  }

  const lab = document.querySelector("[data-lab]");
  if (lab) {
    const value = (id) => Number($(id).value);
    const f = (number, digits = 2) => number.toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits });
    function updateLab() {
      lab.querySelectorAll("input[type=range]").forEach((input) => {
        $(`${input.id}-value`).textContent = `${Number(input.value).toLocaleString("en-US")} ${input.dataset.unit}`;
      });
      let result;
      if (lab.dataset.lab === "ohm") {
        result = CircuitMath.ohm(value("voltage"), value("resistance"));
        $("lab-result").innerHTML = result ? `<small>流過電阻的電流</small><strong>${f(result.currentMA)} mA</strong><p>電阻消耗功率：${f(result.powerMW)} mW</p><p>I = V / R · P = V² / R</p>` : "請輸入有效的電壓與正電阻。";
      } else if (lab.dataset.lab === "divider") {
        result = CircuitMath.divider(value("vin"), value("r1"), value("r2"), value("load"));
        $("lab-result").innerHTML = result ? `<small>帶負載的輸出電壓</small><strong>${f(result.loaded)} V</strong><p>無負載：${f(result.unloaded)} V</p><p>R₂ ∥ Rᴸ = ${f(result.parallel)} Ω</p><p>相對無負載下降 ${f(result.dropPercent, 1)}%</p>` : "請使用正值電阻與有效的輸入電壓。";
      } else if (lab.dataset.lab === "rc") {
        result = CircuitMath.rc(value("rc-r"), value("rc-c"), value("time"));
        $("lab-result").innerHTML = result ? `<small>電容電壓 Vc</small><strong>${f(result.voltage)} V</strong><p>τ = ${f(result.tau, 3)} s · t = ${f(result.time, 3)} s</p><p>充電進度：${f(result.percent, 1)}%</p>` : "請使用正值電阻、電容與非負時間。";
        const path = Array.from({ length: 101 }, (_, i) => {
          const x = 42 + 410 * i / 100;
          const y = 165 - 145 * (1 - Math.exp(-5 * i / 100));
          return `${i ? "L" : "M"}${x.toFixed(2)},${y.toFixed(2)}`;
        }).join(" ");
        $("rc-curve").setAttribute("d", path);
        if (result) {
          $("rc-point").setAttribute("cx", String(42 + 410 * value("time") / 5));
          $("rc-point").setAttribute("cy", String(165 - 145 * result.percent / 100));
          $("rc-chart").setAttribute("aria-label", `RC充電曲線，時間為 ${f(result.time, 3)} 秒，電容電壓 ${f(result.voltage)} V。`);
        }
      }
    }
    lab.querySelectorAll("input[type=range]").forEach((input) => input.addEventListener("input", updateLab));
    updateLab();
  }
}

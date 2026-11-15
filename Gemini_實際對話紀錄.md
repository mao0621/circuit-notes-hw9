# Gemini 實際對話紀錄

這份紀錄保留 Gemini 的專案規劃、程式生成、修正與逐段解釋。可執行的教學範例及網站完整程式收錄於同一份筆記本。

模型：Gemini 3.1 Pro；模式：中等。

對話網址：[https://gemini.google.com/app/b4f33b08d5af2a4d](https://gemini.google.com/app/b4f33b08d5af2a4d)

## 第 1 輪：規劃 AGENTS.md 與網站結構

```text
我要建立第九週作業：Circuit Notes 電路筆記工坊。請用繁體中文設計一份可重複使用的 AGENTS.md。專案用 Python 標準庫把 content/lessons/*.json 產生 docs/ 靜態網站，部署 GitHub Pages。課文有 slug、title、summary、category、difficulty、minutes、order、tags、objectives、sections、pitfalls、exercise、lab、sources。先做歐姆定律、分壓器、RC時間常數。請具體規定檔案命名、新增第四篇流程、資料驗證、單位換算、無障礙與測試；不可只做一次性的網頁。先給架構與規則，不需要程式碼。
```

## 第 1 輪：Gemini 原始回覆

```text
這是一份為 AI 代理（AI Agents）與協作者設計的 AGENTS.md 系統提示與規範文件。這份文件的目標是確保專案具備高度的可重複使用性與擴展性，讓 AI 在未來維護或新增內容時，能嚴格遵守資料夾結構、命名習慣與驗證邏輯，避免產生一次性的免洗網頁。

以下為 AGENTS.md 的架構與規則設計：

AGENTS.md：Circuit Notes 電路筆記工坊開發與維護規範
1. 專案概述 (Project Overview)

本專案為靜態電路學習網站，利用 Python 標準庫（如 json, os, pathlib, html 等，禁用第三方套件）將結構化的 JSON 內容轉換為靜態 HTML 網頁，輸出至 docs/ 資料夾，並透過 GitHub Pages 部署。

初始內容：歐姆定律 (Ohm's Law)、分壓器 (Voltage Divider)、RC 時間常數 (RC Time Constant)。

開發原則：系統必須是模組化且資料驅動（Data-Driven），嚴禁將特定課程的邏輯寫死於 Python 渲染腳本中。

2. 目錄與檔案命名規範 (Naming Conventions)

AI 代理在讀寫檔案時，必須嚴格遵守以下命名與結構：

來源內容區：content/lessons/

JSON 檔案命名公式：[order]-[slug].json（皆為小寫，以連字號分隔，並補零至兩位數）。

範例：01-ohms-law.json, 02-voltage-divider.json, 03-rc-time-constant.json。

靜態輸出區：docs/

生成的網頁命名公式：[slug].html（例如 ohms-law.html）。

首頁：docs/index.html（由 Python 讀取所有 JSON 動態生成課程列表）。

靜態資源區：docs/assets/

圖片與圖表命名：[slug]-[image-name].[ext]（例如 ohms-law-schematic.svg）。

3. 資料結構與驗證 (Data Validation)

在生成網頁前，腳本必須驗證 JSON 檔案是否具備以下所有鍵值（Keys）且符合型態：

slug (String): 網址與檔名友善字串（僅限小寫字母、數字與連字號）。

title (String): 課程標題（例如「RC時間常數」）。

summary (String): 簡短的一句話介紹。

category (String): 分類（例如 "DC Circuits", "AC Circuits"）。

difficulty (Enum): 嚴格限制為 "Beginner", "Intermediate", "Advanced" 三者之一。

minutes (Integer): 預估學習分鐘數，必須 > 0。

order (Integer): 課程排序權重，決定生成目錄的順序。

tags (Array of Strings): 概念標籤（例如 ["Resistor", "Capacitor"]）。

objectives (Array of Strings): 學習目標列表。

sections (Array of Objects): 課文主體，包含 heading (子標題) 與 content (段落內容，支援基本 HTML/Markdown)。

pitfalls (Array of Strings): 常見錯誤與迷思概念。

exercise (Object): 包含 question (題目) 與 answer (解答)。

lab (Object): 實作或模擬環節建議，包含 materials (材料) 與 steps (步驟)。

sources (Array of Strings): 參考資料或延伸閱讀連結。

4. 單位換算處理 (Unit Conversion & Formatting)

電路筆記會大量使用物理單位，腳本與資料建立時必須遵循「標準化與易讀性」規則：

JSON 資料儲存格式：底層數據（如題目數值）應盡量使用科學記號或標準單位（如 V, A, Ohm, F, H）。

渲染顯示格式：網頁生成時，若遇到單位表示，需遵循工程前綴規範（Engineering Prefixes）。

範例：1000 Ohm 應渲染為 1 kΩ。

範例：0.000001 F 應渲染為 1 µF。

避免在內文中混用中英文縮寫（例如不要寫「1千歐姆」，統一使用「1 kΩ」）。

5. 無障礙與語意化設計 (Accessibility & A11y)

生成的 HTML 檔案必須符合 WCAG 基本無障礙規範：

語意化標籤：使用 <main>, <article>, <section>, <aside> (用於 pitfalls) 建立清晰文件大綱。

圖片與圖表：所有電路圖皆需包含描述性的 alt 屬性（例如：alt="包含一個 10V 電源與兩個串聯電阻的分壓器電路圖"）。

數學公式與符號：特殊符號（如 Ω, µ）或數學公式區塊，需確保螢幕閱讀器能正確解析，或給予 aria-label 輔助說明。

色彩對比：警告區塊（Pitfalls）不可僅依賴顏色傳達資訊，必須加上文字提示（如「⚠️ 注意：」）。

6. 新增第四篇課程的工作流程 (Workflow for Adding Lesson 4)

當使用者要求 AI 代理新增第四篇課程（例如「克希荷夫定律」）時，請嚴格執行以下流程：

分析階段：確認課程主題，規劃 JSON 結構所需的知識點。

建立草稿：在 content/lessons/ 下建立 04-kirchhoffs-laws.json。

填寫資料：完整填寫所有必備的欄位（包含 objectives, sections, pitfalls, exercise 等）。

驗證階段：模擬執行 Python 驗證邏輯，確認該 JSON 沒有遺漏必填欄位，且難度 Enum 拼字正確。

重新編譯：提示使用者執行 Python 生成腳本，將新 JSON 轉換為 docs/kirchhoffs-laws.html，並確保其自動被加入到 docs/index.html 的目錄清單中。

7. 測試與驗證規範 (Testing & Quality Assurance)

在沒有使用第三方套件（如 pytest）的情況下，AI 應設計原生 Python assert 測試或檢查機制：

JSON Schema 檢查：腳本執行前，先掃描 content/lessons/*.json 確保沒有 Key 缺失或型別錯誤。

連結死鏈測試 (Broken Link Check)：生成 HTML 後，腳本應檢查內部連結（如 <a href="ohms-law.html">）是否指向實際存在的生成的檔案。

網頁基本結構測試：確保每個生成的 HTML 都包含 <title>、正確的 <meta charset="UTF-8"> 以及響應式 viewport 設定。

這份 AGENTS.md 已經定義了清楚的邊界與規則。接下來，您希望從哪個部分開始實作？
設計前三篇的 JSON 結構資料
規劃 Python 靜態網站生成腳本
```

## 第 2 輪：生成 Python 驗證與渲染初稿

```text
延續上面的電路筆記工坊。先沿用一個 <slug>.json 對應一課（order 排序），difficulty 為入門或進階，段落使用 paragraphs，lab 只用 ohm/divider/rc/none。請直接寫一個可在 Colab 執行的 Python 標準庫教學範例：完整函式驗證 slug 與檔名一致，再用 html.escape 安全組合課文標題與段落，附可跑的 assert 正反案例。程式請放同一個 code block，不用安裝套件。
```

## 第 2 輪：Gemini 原始回覆

```text
這是一份完全使用 Python 標準庫、可直接貼入 Google Colab 執行的教學範例。程式碼包含了嚴格的資料驗證（檔名與 slug 一致性、Enum 限制）、使用 html.escape 防範 XSS 的安全渲染，以及完整的正反面 assert 測試案例。

Python
import json
import os
import html
import tempfile
from pathlib import Path

# ==========================================
# 1. 核心邏輯：資料驗證與 HTML 生成
# ==========================================

def validate_lesson(file_path: str, data: dict) -> bool:
    """
    驗證電路筆記的 JSON 資料結構與檔名一致性。
    若驗證失敗會拋出 ValueError。
    """
    # 1. 檢查必填欄位
    required_keys = {"slug", "title", "order", "difficulty", "paragraphs", "lab"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"驗證失敗: 缺少必要欄位 {missing}")

    # 2. 驗證 slug 與檔名是否完全一致 (例如檔案名為 ohms-law.json，slug 必須為 ohms-law)
    file_stem = Path(file_path).stem  # 取得不含副檔名的檔名
    if file_stem != data["slug"]:
        raise ValueError(f"驗證失敗: 檔名 ({file_stem}.json) 與 JSON 內的 slug ({data['slug']}) 不一致！")

    # 3. 驗證欄位 Enum 限制
    if data["difficulty"] not in ["入門", "進階"]:
        raise ValueError(f"驗證失敗: difficulty 必須為 '入門' 或 '進階'，目前為 '{data['difficulty']}'")
        
    if data["lab"] not in ["ohm", "divider", "rc", "none"]:
        raise ValueError(f"驗證失敗: lab 必須為 ohm, divider, rc, none 之一，目前為 '{data['lab']}'")

    # 4. 驗證段落結構
    if not isinstance(data["paragraphs"], list) or not all(isinstance(p, str) for p in data["paragraphs"]):
        raise ValueError("驗證失敗: paragraphs 必須是字串列表 (List of Strings)")

    return True

def generate_lesson_html(data: dict) -> str:
    """
    安全地將 JSON 轉換為靜態 HTML，強制使用 html.escape 防禦 XSS 攻擊。
    """
    # 安全跳脫標題
    safe_title = html.escape(data["title"])
    safe_difficulty = html.escape(data["difficulty"])
    safe_lab = html.escape(data["lab"])
    
    # 安全跳脫每一個段落，並組合為 HTML 段落標籤
    safe_paragraphs = []
    for p in data["paragraphs"]:
        # 轉換前：V = I * R (包含危險字元的話會被跳脫，例如 <script>)
        safe_p = html.escape(p)
        safe_paragraphs.append(f"        <p>{safe_p}</p>")
    
    paragraphs_html = "\n".join(safe_paragraphs)

    # 組合完整 HTML (使用語意化標籤)
    html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Circuit Notes</title>
</head>
<body>
    <main>
        <header>
            <h1>{safe_title}</h1>
            <div class="meta">
                <span>難度：{safe_difficulty}</span> | <span>實驗室：{safe_lab}</span>
            </div>
        </header>
        <article>
{paragraphs_html}
        </article>
    </main>
</body>
</html>"""
    return html_template


# ==========================================
# 2. 測試環境與 Assert 驗證案例
# ==========================================

def run_tests():
    print("開始執行測試案例...\n")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        
        # ------------------------------------------------
        # 測試案例 1：完全合規的正向測試 (Positive Test)
        # ------------------------------------------------
        valid_json_path = os.path.join(tmpdir, "ohms-law.json")
        valid_data = {
            "slug": "ohms-law",
            "title": "歐姆定律 (Ohm's Law)",
            "order": 1,
            "difficulty": "入門",
            "paragraphs": [
                "歐姆定律是電路學中最基礎的定律。",
                "公式為 V = I * R，其中 V 是電壓，I 是電流，R 是電阻。",
                "注意：遇到 <短路> 情況時，電流 I 會趨近於無限大。" # 包含需 Escape 的字元
            ],
            "lab": "ohm"
        }
        
        # 寫入暫存檔
        with open(valid_json_path, "w", encoding="utf-8") as f:
            json.dump(valid_data, f, ensure_ascii=False)
        
        # 讀取並驗證
        with open(valid_json_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            
        try:
            assert validate_lesson(valid_json_path, loaded_data) == True, "正向測試失敗！"
            print("✅ 測試 1 通過：合規的 JSON 通過驗證。")
            
            # 測試 HTML 渲染與 Escape 檢查
            html_output = generate_lesson_html(loaded_data)
            assert "&lt;短路&gt;" in html_output, "HTML 跳脫失敗！危險字元未被 escape。"
            print("✅ 測試 2 通過：HTML 成功生成且特殊字元已安全跳脫。")
            print("-" * 40)
            print("生成預覽 (部分)：")
            print("\n".join(html_output.split("\n")[15:19])) # 印出段落區塊
            print("-" * 40 + "\n")
            
        except AssertionError as e:
            print(f"❌ 正向測試發生非預期錯誤: {e}")

        # ------------------------------------------------
        # 測試案例 3：檔名與 slug 不一致 (Negative Test)
        # ------------------------------------------------
        invalid_slug_path = os.path.join(tmpdir, "wrong-file-name.json")
        try:
            validate_lesson(invalid_slug_path, valid_data) # 資料裡面的 slug 是 ohms-law
            assert False, "應阻擋不一致的檔名，但卻通過了！"
        except ValueError as e:
            assert "檔名" in str(e) and "不一致" in str(e)
            print(f"✅ 測試 3 通過：成功阻擋 slug 與檔名不一致 ({e})")

        # ------------------------------------------------
        # 測試案例 4：不合法的 difficulty (Negative Test)
        # ------------------------------------------------
        invalid_difficulty_data = valid_data.copy()
        invalid_difficulty_data["difficulty"] = "專家" # 規定只能入門或進階
        try:
            validate_lesson(valid_json_path, invalid_difficulty_data)
            assert False, "應阻擋錯誤的 difficulty Enum，但卻通過了！"
        except ValueError as e:
            assert "difficulty 必須為" in str(e)
            print(f"✅ 測試 4 通過：成功阻擋非法的難度標籤 ({e})")

        # ------------------------------------------------
        # 測試案例 5：不合法的 lab (Negative Test)
        # ------------------------------------------------
        invalid_lab_data = valid_data.copy()
        invalid_lab_data["lab"] = "kirchhoff" # 不在 ohm, divider, rc, none 之中
        try:
            validate_lesson(valid_json_path, invalid_lab_data)
            assert False, "應阻擋錯誤的 lab Enum，但卻通過了！"
        except ValueError as e:
            assert "lab 必須為" in str(e)
            print(f"✅ 測試 5 通過：成功阻擋非法的實驗分類 ({e})")

    print("\n🎉 所有單元測試皆順利通過！")

if __name__ == "__main__":
    run_tests()

```

## 第 3 輪：修正 sections 結構及測試

```text
剛才的初稿用了頂層 paragraphs，實際資料是 sections（每節有 heading 與 paragraphs）。請給我修正版完整可跑的一個 Python code block：用正規表示式驗證 kebab-case、確認副檔名 .json 和 slug 一致、order 是正整數（bool 不算）、sections 非空且段落皆非空字串，維持 difficulty 與 lab 的限制。安全渲染 heading/title/段落；測試失敗要讓 Colab 儲存格停止，不要 catch AssertionError 後仍印通過。附小型正反測例，盡量 100 行內。
```

## 第 3 輪：Gemini 原始回覆

```text
這是一份符合您要求、完全使用標準庫且能在 Colab 單一儲存格執行的 Python 腳本。

這次將資料結構升級為 sections，並加入嚴格的型別檢查（剔除 bool 偽裝成 int 的情況）、正則表達式驗證 kebab-case。測試環節也移除了對 AssertionError 的攔截，只要有任何驗證邏輯瑕疵，儲存格就會直接拋出異常並亮紅燈停止執行。

Python
import json
import os
import html
import tempfile
import re
from pathlib import Path

# ==========================================
# 1. 核心邏輯：資料驗證與 HTML 生成
# ==========================================
def validate_lesson(file_path: str, data: dict) -> bool:
    # 1. 檢查必填欄位
    req_keys = {"slug", "title", "order", "difficulty", "lab", "sections"}
    if missing := req_keys - data.keys():
        raise ValueError(f"缺少必要欄位: {missing}")

    # 2. kebab-case 與檔名一致性檢查
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", data["slug"]):
        raise ValueError("slug 必須為小寫 kebab-case 格式")
    if Path(file_path).stem != data["slug"]:
        raise ValueError(f"檔名 ({Path(file_path).stem}) 與 slug ({data['slug']}) 不一致")

    # 3. 檢查 order 為嚴格正整數 (Python 中 bool 是 int 的子類，需用 type 排除)
    if type(data["order"]) is not int or data["order"] <= 0:
        raise ValueError("order 必須為正整數（不可為 boolean 或 0）")

    # 4. Enum 檢查
    if data["difficulty"] not in ["入門", "進階"]: raise ValueError("difficulty 錯誤")
    if data["lab"] not in ["ohm", "divider", "rc", "none"]: raise ValueError("lab 錯誤")

    # 5. Sections 結構與空值檢查
    if not isinstance(data["sections"], list) or not data["sections"]:
        raise ValueError("sections 必須為非空陣列")

    for sec in data["sections"]:
        if "heading" not in sec or "paragraphs" not in sec:
            raise ValueError("節 (section) 缺少 heading 或 paragraphs")
        if not isinstance(sec["heading"], str):
            raise ValueError("heading 必須為字串")
        if not isinstance(sec["paragraphs"], list) or not sec["paragraphs"]:
            raise ValueError("paragraphs 必須為非空陣列")
            
        for p in sec["paragraphs"]:
            # 確保段落是字串，且去除空白後不為空
            if not isinstance(p, str) or not p.strip():
                raise ValueError("段落不可為空字串或純空白字元")

    return True

def generate_html(data: dict) -> str:
    # 安全渲染所有暴露的文字內容
    html_out = [f"<h1>{html.escape(data['title'])}</h1>"]
    html_out.append(f"<div class='meta'>難度: {html.escape(data['difficulty'])} | Lab: {html.escape(data['lab'])}</div>")
    
    for sec in data["sections"]:
        html_out.append(f"  <h2>{html.escape(sec['heading'])}</h2>")
        for p in sec["paragraphs"]:
            html_out.append(f"  <p>{html.escape(p)}</p>")
            
    return "\n".join(html_out)


# ==========================================
# 2. 單元測試 (Colab 執行區)
# ==========================================
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        valid_path = os.path.join(tmpdir, "ohms-law.json")
        valid_data = {
            "slug": "ohms-law", "title": "歐姆定律 <Ohm>", "order": 1, 
            "difficulty": "入門", "lab": "ohm",
            "sections": [
                {"heading": "公式 & 介紹", "paragraphs": ["V = I * R", "遇到 <短路> 情況..."]}
            ]
        }
        with open(valid_path, "w", encoding="utf-8") as f:
            json.dump(valid_data, f)

        # -------------------------
        # [正向測試] 合規資料
        # -------------------------
        with open(valid_path, "r", encoding="utf-8") as f: loaded = json.load(f)
        assert validate_lesson(valid_path, loaded), "正向測試失敗"
        
        html_res = generate_html(loaded)
        assert "&lt;Ohm&gt;" in html_res, "Title 跳脫失敗"
        assert "&amp; 介紹" in html_res, "Heading 跳脫失敗"
        assert "&lt;短路&gt;" in html_res, "Paragraph 跳脫失敗"

        # -------------------------
        # [負向測試] 預期需觸發 ValueError，否則 assert 讓程式崩潰
        # -------------------------
        def expect_validation_error(mod_data, err_keyword, path=valid_path):
            try:
                validate_lesson(path, mod_data)
                raise AssertionError(f"應阻擋但卻通過了！測試情境: 預期錯誤 '{err_keyword}'")
            except ValueError as e:
                assert err_keyword in str(e), f"預期攔截 '{err_keyword}'，實際錯誤為 '{e}'"

        # 測試 1: slug 不是 kebab-case
        bad_slug = valid_data.copy()
        bad_slug["slug"] = "Ohm_Law"
        expect_validation_error(bad_slug, "kebab-case", os.path.join(tmpdir, "Ohm_Law.json"))

        # 測試 2: order 偽裝成 boolean
        bad_order = valid_data.copy()
        bad_order["order"] = True  
        expect_validation_error(bad_order, "正整數")

        # 測試 3: section 內有空白段落字串
        bad_section = valid_data.copy()
        bad_section["sections"] = [{"heading": "測試", "paragraphs": ["  "]}] 
        expect_validation_error(bad_section, "空字串")

        # 測試 4: 缺少 heading
        bad_keys = valid_data.copy()
        bad_keys["sections"] = [{"paragraphs": ["正常內容"]}]
        expect_validation_error(bad_keys, "缺少 heading")

        print("✅ 所有 1 個正向與 4 個負向測試皆通過，防護機制完全生效！")

```

## 第 4 輪：逐段解釋程式並生成電路公式

```text
請把剛才修正版逐段用繁體中文解釋給 Python 初學者：輸入長什麼樣、kebab-case 和副檔名為何都要驗證、為何 type(x) is int 不接受 True、sections 的巢狀走訪、html.escape 前後例子、正反測試各證明什麼。請再給一個短小可直接跑的 Python code block：用三個純函式實作歐姆定律 I=V/R、空載分壓 Vout=Vin*R2/(R1+R2)、RC 充電的 tau 和 Vc（電阻為 Ω、電容為 F、時間為秒），附正值檢查和可核對的 assert，並逐段解釋公式和單位。
```

## 第 4 輪：Gemini 原始回覆

```text
這是一份為 Python 初學者準備的程式碼逐段解析，以及將你所學的基礎電路理論轉化為嚴謹程式碼的實作。

第一部分：前版 Python 驗證程式碼原理解析

1. 輸入資料長什麼樣？
輸入的是一個 Python 字典（Dictionary），這通常是從 JSON 檔案讀取進來的。它就像一個有標籤的收納盒：

Python
{
    "slug": "ohms-law",
    "title": "歐姆定律",
    "order": 1,
    # ...其他屬性...
    "sections": [
        {
            "heading": "公式介紹",
            "paragraphs": ["V = I * R", "段落二..."]
        }
    ]
}


2. 為什麼 kebab-case 和「副檔名」都要驗證？

kebab-case 是指「全小寫且用連字號分隔」（例如 ohms-law）。這是為了確保網址（URL）美觀且在所有作業系統下都不會因為大小寫或空白產生抓取錯誤。

與副檔名一致 是為了「資料連動」。如果檔案叫 rc-circuit.json，但裡面的 slug 卻寫 ohms-law，未來在生成網站目錄或設定超連結 <a href="ohms-law.html"> 時，就會對應錯檔案，產生「死鏈（Broken Link）」。兩者一致能保證「檔名就是網址 ID」。

3. 為何 type(x) is int 不接受 True？
這是一個 Python 特有的陷阱。在 Python 底層，布林值（bool）其實是整數（int）的子類別：True 等於 1，False 等於 0。
如果你只寫 isinstance(True, int)，Python 會回傳 True，導致原本用來設定課程排序的 order 欄位不小心被塞入 True。改用 type(x) is int 是「嚴格比對型別」，確保它必須是貨真價實的整數型別。

4. sections 的巢狀走訪 (Nested Iteration)
處理結構化資料就像剝洋蔥，因為 sections 是一個「列表裡面裝字典，字典裡面又裝列表」，我們必須用兩層迴圈：

Python
for sec in data["sections"]:      # 第一層：翻開每一個「小節」
    # 這裡可以讀到 sec['heading']
    for p in sec["paragraphs"]:   # 第二層：讀取這個小節內的每一個「段落」
        # 這裡才真正讀到裡面的文字


5. html.escape 前後例子與作用
瀏覽器看到 < 和 > 會以為那是 HTML 標籤或 JavaScript 腳本。如果有人在 JSON 的標題惡意寫入腳本，或者電路筆記裡寫了 <短路>，瀏覽器會因為看不懂 <短路> 標籤而把字吃掉。

轉換前：遇到 <短路> 時，電流會變大，請看 <script>alert("中毒")</script>

轉換後：遇到 &lt;短路&gt; 時，電流會變大，請看 &lt;script&gt;alert("中毒")&lt;/script&gt;html.escape 會把特殊字元變成「安全編碼」，讓瀏覽器「純顯示字串」而不去執行它。

6. 正反測試（Positive / Negative Tests）各證明什麼？

正向測試：證明「正確的資料能順利通關並產出預期的 HTML」，代表程式有基本工作能力。

負向測試：故意餵給程式「錯誤的資料」（如空字串、偽裝的布林值），證明「程式的防護網（Guardrails）確實能把不合規的資料攔截下來並報錯」，這在嚴謹的系統中比正向測試更重要。

第二部分：電路學公式實作與驗證

針對你熟悉的電路學理論，這裡使用「純函式 (Pure Functions)」實作。純函式的特點是：只要輸入相同，保證輸出相同，且不會修改外部狀態。

Python
import math

def calc_ohm_current(v: float, r: float) -> float:
    """計算歐姆定律電流 I = V / R"""
    if r <= 0:
        raise ValueError("電阻 R 必須大於 0 Ω")
    return v / r

def calc_voltage_divider(vin: float, r1: float, r2: float) -> float:
    """計算空載分壓電路輸出電壓 Vout = Vin * [R2 / (R1 + R2)]"""
    if r1 <= 0 or r2 <= 0:
        raise ValueError("分壓電阻 R1 與 R2 必須大於 0 Ω")
    return vin * (r2 / (r1 + r2))

def calc_rc_charging(vin: float, r: float, c: float, t: float) -> tuple[float, float]:
    """
    計算 RC 充電電路的 時間常數 (tau) 與 特定時間下的電容電壓 (Vc)
    回傳值：(tau, vc)
    """
    if r <= 0: raise ValueError("電阻 R 必須大於 0 Ω")
    if c <= 0: raise ValueError("電容 C 必須大於 0 F")
    if t < 0:  raise ValueError("時間 t 不可為負數")
    
    tau = r * c
    # 公式：Vc(t) = Vin * (1 - e^(-t/tau))
    vc = vin * (1 - math.exp(-t / tau)) 
    return tau, vc

# ==========================================
# Assert 測試驗證區
# ==========================================
if __name__ == "__main__":
    # 1. 歐姆定律測試 (10V, 5Ω -> 2A)
    assert calc_ohm_current(10, 5) == 2.0, "歐姆定律計算錯誤"
    try:
        calc_ohm_current(10, 0)
        assert False, "應阻擋 0 歐姆"
    except ValueError:
        pass

    # 2. 分壓器測試 (10V, R1=100Ω, R2=100Ω -> 5V)
    assert calc_voltage_divider(10, 100, 100) == 5.0, "分壓器計算錯誤"

    # 3. RC 充電測試 
    # 假設 10V 電源，R=1kΩ (1000Ω)，C=1mF (0.001F)
    # 時間常數 tau = 1000 * 0.001 = 1 秒
    # 經過 1 個 tau (t=1) 時，Vc 約為 6.321V (即充電達 63.2%)
    tau, vc = calc_rc_charging(10, 1000, 0.001, 1)
    
    assert tau == 1.0, f"時間常數錯誤，預期 1.0，實際為 {tau}"
    # 因為浮點數算 e 會產生極微小誤差，我們使用 math.isclose 容許 0.001 的誤差
    assert math.isclose(vc, 6.321, abs_tol=0.001), f"RC 電壓錯誤，實際計算為 {vc}"
    
    print("✅ 三個電路函式與正值防護測試皆順利通過！")


公式與單位逐段解析：

歐姆定律 (calc_ohm_current)

公式：
𝐼
=
𝑉
𝑅
I=
R
V
	​


單位：輸入 
𝑉
V 為伏特 (V)、
𝑅
R 為歐姆 (Ω)，輸出 
𝐼
I 為安培 (A)。

設計邏輯：理想電線電阻為 0，但在這裡作為除數，若 
𝑅
=
0
R=0 會引發除以零錯誤（ZeroDivisionError），因此加上 r <= 0 的防護網。

空載分壓器 (calc_voltage_divider)

公式：
𝑉
𝑜
𝑢
𝑡
=
𝑉
𝑖
𝑛
×
𝑅
2
𝑅
1
+
𝑅
2
V
out
	​

=V
in
	​

×
R
1
	​

+R
2
	​

R
2
	​

	​


單位：阻值 
𝑅
1
,
𝑅
2
R
1
	​

,R
2
	​

 為歐姆 (Ω)，輸入與輸出電壓為伏特 (V)。

設計邏輯：「空載」代表沒有接其他負載電阻抽取電流，所以電流完全遵守串聯公式 
𝐼
=
𝑉
𝑖
𝑛
𝑅
1
+
𝑅
2
I=
R
1
	​

+R
2
	​

V
in
	​

	​

，而 
𝑉
𝑜
𝑢
𝑡
V
out
	​

 就是量測 
𝑅
2
R
2
	​

 兩端的電壓 (
𝐼
×
𝑅
2
I×R
2
	​

)。

RC 充電 (calc_rc_charging)

公式：
𝜏
=
𝑅
×
𝐶
τ=R×C ； 
𝑉
𝑐
(
𝑡
)
=
𝑉
𝑖
𝑛
×
(
1
−
𝑒
−
𝑡
𝜏
)
V
c
	​

(t)=V
in
	​

×(1−e
−
τ
t
	​

)

單位：
𝑅
R 為歐姆 (Ω)、
𝐶
C 必須使用法拉 (F)（若是常見的 
𝜇
𝐹
μF 必須轉換為 
10
−
6
𝐹
10
−6
F 傳入）、時間 
𝑡
t 為秒 (s)。

設計邏輯：Python 內建的 math.exp(x) 等同於數學上的 
𝑒
𝑥
e
x
。這是一個隨時間逼近飽和的步階響應，經過 1 倍時間常數 (
𝜏
τ) 時，電壓會達到電源的約 63.2%，經過 5 倍 
𝜏
τ 時可視為完全充飽 (99.3%)。這與你在電子學分析二階或積分器電路時的暫態行為核心概念是一致的。
```

## 第 5 輪：補上副檔名與格式邊界，整理網站各模組

```text
我檢查程式時發現 Path(...).stem 不會驗證副檔名，而 re.match 的 $ 可能允許末尾換行。請給一小段可執行的 Python 補丁示例：用 Path.suffix 與 re.fullmatch，確認錯副檔名與尾端換行會被拒絕。接著幫我寫四小段 Markdown 學習筆記，對應本專案：JSON 資料與 Python 共用 HTML 模板如何串起來、CSS 的色票與響應式版面作用、JavaScript localStorage 搜尋/收藏與三種公式的角色、驗收為何要檢查新增第四篇和斷連結。每段說明輸入、處理、輸出，再附一個可自行嘗試的小練習，請不要聲稱你執行了網站測試。
```

## 第 5 輪：Gemini 原始回覆

```text
Python
import re
from pathlib import Path

def validate_filename_and_slug_strict(file_path: str, slug: str) -> bool:
    """修補版：嚴格驗證副檔名與字串邊界"""
    p = Path(file_path)
    
    # 1. 嚴格驗證副檔名 (Path.suffix 會包含點，如 '.json')
    if p.suffix.lower() != '.json':
        raise ValueError(f"副檔名錯誤：預期 .json，實際為 {p.suffix}")
        
    # 2. 驗證主檔名 (stem) 與 slug 一致
    if p.stem != slug:
        raise ValueError(f"檔名 ({p.stem}) 與 slug ({slug}) 不一致")
        
    # 3. 嚴格驗證 kebab-case
    # re.fullmatch 強制整個字串完全符合 pattern，消除了 match 搭配 $ 時對末尾 \n 的寬容
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise ValueError("slug 必須為嚴格的 kebab-case，不可包含換行或非法字元")
        
    return True

if __name__ == "__main__":
    # [正向測試]
    assert validate_filename_and_slug_strict("content/ohms-law.json", "ohms-law")
    
    # [負向測試 1] 阻擋錯誤的副檔名
    try:
        validate_filename_and_slug_strict("content/ohms-law.txt", "ohms-law")
        assert False, "應阻擋 .txt 副檔名"
    except ValueError as e:
        assert ".json" in str(e)
        
    # [負向測試 2] 阻擋末尾換行漏洞 (模擬讀取檔案時未 strip() 的情況)
    try:
        validate_filename_and_slug_strict("content/ohms-law\n.json", "ohms-law\n")
        assert False, "應阻擋末尾換行"
    except ValueError as e:
        assert "kebab-case" in str(e)
        
    print("✅ 補丁測試通過：已成功阻擋錯副檔名與末尾換行漏洞！")

筆記一：JSON 資料與 Python HTML 模板的資料驅動架構

將內容與介面分離是專案可維護性的核心。

輸入 (Input)：結構化的 JSON 檔案（例如包含 title, sections 等純文字資料）。

處理 (Process)：Python 讀取 JSON，利用 html.escape 清洗危險字元後，將資料注入準備好的 HTML f-string 模板，並透過迴圈將巢狀結構（如段落）展開為 HTML 標籤（<p>、<h2>）。

輸出 (Output)：純靜態的 .html 檔案，準備供瀏覽器讀取。

動手做小練習：在 Python 腳本的 HTML 模板字串最後，試著加入一段包含當前年份的 <footer>&copy; 2026 電路筆記</footer>，重新執行並用瀏覽器開啟生成的檔案檢查結果。

筆記二：CSS 色票與響應式版面的視覺工程

網頁不只要能看，還要適應不同裝置並維持品牌一致性。

輸入 (Input)：生成的無樣式 HTML 元素（DOM Tree）與使用者的裝置螢幕寬度（Viewport）。

處理 (Process)：CSS 引擎比對選擇器。透過 CSS 變數（如 --primary: #0056b3;）統一全站的色票，並透過媒體查詢（Media Queries）在特定斷點改變版面邏輯（如從並排的 Grid 變為垂直堆疊的 Flexbox）。

輸出 (Output)：在桌機大螢幕上顯示清晰的兩欄式電路圖文，在手機上自動摺疊為單欄易讀版面。

動手做小練習：在你的 CSS 檔寫入 @media (max-width: 600px) { body { background-color: #f0f0f0; } }，然後把瀏覽器視窗拉窄，觀察背景顏色的變化。

筆記三：JS localStorage 與電路公式的角色

前端 JavaScript 賦予靜態網頁互動能力與狀態記憶，這是二階電路暫態分析或實驗室數據紀錄的好幫手。

輸入 (Input)：使用者點擊「收藏」按鈕，或在實驗室小工具輸入電阻與電容數值（例如 
𝑅
=
1000
,
𝐶
=
0.001
R=1000,C=0.001）。

處理 (Process)：

localStorage：JS 捕捉點擊事件，將狀態寫入瀏覽器的本機儲存空間（如 localStorage.setItem('fav_rc', 'true')）。

電路公式：JS 讀取輸入值，執行歐姆定律、分壓定理或 RC 充電公式的純函式計算。

輸出 (Output)：重新整理網頁後，收藏星號依然亮著；畫面上即時顯示計算出的時間常數 
𝜏
τ 或目標電壓，無需伺服器介入。

動手做小練習：按 F12 打開開發者工具的 Console，輸入 localStorage.setItem('user', 'EECS')，接著按重新整理，再輸入 localStorage.getItem('user')，看看瀏覽器是否記住了。

筆記四：架構驗收（第四篇擴充與斷鏈檢查）

我們不是在做「一次性網頁」，驗收是為了證明系統的擴展性。

輸入 (Input)：在 content/lessons/ 新增一份 04-kirchhoffs-laws.json，以及專案內所有的 HTML 連結標籤 <a href="...">。

處理 (Process)：

擴充性測試：不修改任何 Python 程式碼，直接重新執行腳本，檢查 Python 的目錄掃描邏輯是否自動抓取了新 JSON。

斷鏈測試：爬蟲腳本讀取生成的 HTML，萃取所有 href 屬性，並使用 os.path.exists() 檢查目標檔案是否確實存在。

輸出 (Output)：產生完整的 4 課目錄首頁；若有連結打錯字指向不存在的檔案，系統會在部署前主動報錯。

動手做小練習：寫一個 3 行的 Python 腳本，使用 import os，檢查目前資料夾底下是否存在 04-kirchhoffs-laws.json（print(os.path.exists('...'))）。
```

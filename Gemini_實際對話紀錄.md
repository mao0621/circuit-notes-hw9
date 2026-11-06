# Gemini 實際對話紀錄

這是實際使用 Gemini Pro 中等模式進行的專案規劃對話；最終程式另經整合、修正與驗證。

模型：Gemini 3.1 Pro；模式：中等。

對話網址：[https://gemini.google.com/app/b4f33b08d5af2a4d](https://gemini.google.com/app/b4f33b08d5af2a4d)

## 第 1 輪：Prompt

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

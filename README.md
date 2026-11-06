# Circuit Notes｜電路筆記工坊

一個以繁體中文整理基礎電路觀念的靜態知識庫。每篇筆記都包含學習目標、觀念與公式、易錯提醒、練習及來源；部分課文附有可調參數的互動實驗。

[開啟公開網站](https://mao0621.github.io/circuit-notes-hw9/) · [GitHub Repository](https://github.com/mao0621/circuit-notes-hw9)

本專案的重點是建立可重用的內容規則：AI 先閱讀 [AGENTS.md](AGENTS.md)，依固定 JSON 格式新增課文，再由共用模板產生網頁，無須每次重新設計版面。第九週作業主題為「建立自己的 AGENTS.md 或 CLAUDE.md」。

## 目前內容

| 課文 | 內容 | 互動 |
| --- | --- | --- |
| 歐姆定律 | 電壓、電流、電阻與功率 | 改變電壓與電阻，查看電流和功率 |
| 分壓器 | 理想分壓與負載效應 | 調整電阻與輸入，觀察輸出變化 |
| RC 時間常數 | 充電曲線與單位換算 | 調整 R、C 與時間，查看充電電壓 |

第三篇 RC 課文用來示範同一套規則的延伸方式。本次建立三篇內容作為可運作的示例，並未宣稱這些頁面來自過去的課堂實驗。

## 環境與本機瀏覽

需要 Python 3；建置只使用標準函式庫，不需安裝第三方套件。網頁使用原生 HTML、CSS、JavaScript，不依賴外部 CDN。

在專案根目錄執行：

```bash
python build.py
python tests/check_project.py
python -m http.server 8000 --directory docs
```

啟動後開啟 `http://localhost:8000`。停止預覽時，在啟動伺服器的終端機按 `Ctrl+C`。

`build.py` 會由 `content/lessons/*.json` 與 `assets/` 重新產生 `docs/`。請修改來源檔，不要直接修改產出的 HTML。若修改後沒有重建，公開網站仍會顯示舊內容。

## 新增一篇內容

1. 閱讀 [AGENTS.md](AGENTS.md) 的資料格式與內容標準。
2. 複製 `content/template.json`，另存為 `content/lessons/<slug>.json`。
3. 填入全部欄位，核對公式、單位、練習與來源。選用既有互動類型，或設為 `none`。
4. 執行建置、驗收與預覽，確認首頁與新文章都可正常瀏覽。
5. 提交來源檔與更新後的 `docs/`。

可直接交給 AI 的提示詞，以及 RC 延伸示範，見 [docs-authoring.md](docs-authoring.md)。

## 發布到 GitHub Pages

這是一般 Repository 的靜態網站，不需要自訂網域或後端服務。發布狀態與實際連結請以本次發布結果為準。

1. 在自己的 GitHub 帳號建立公開 Repository，將本專案完整上傳到預設分支。確認 Repository 根目錄有 `AGENTS.md`，且 `docs/index.html` 已建置。
2. 開啟 Repository 的 **Settings → Pages**。
3. 在 **Build and deployment** 選擇 **Deploy from a branch**。
4. 選擇實際上傳的分支（通常為 `main`），資料夾選 **`/docs`**，再儲存。
5. 等待 GitHub Pages 部署完成；以 Pages 頁面顯示的真實網址開啟首頁、任一課文及規則頁。不要把預測網址當成成功部署的證明。

頁面採相對路徑，可放在 GitHub Pages 的 Repository 子路徑。每次改內容後，重新建置並推送 `docs/`；Pages 會依其設定部署新的提交。

| 繳交所需項目 | 位置或狀態 |
| --- | --- |
| 專案簡介 | 本 README 首段 |
| GitHub Repository 連結 | [mao0621/circuit-notes-hw9](https://github.com/mao0621/circuit-notes-hw9) |
| 網頁連結 | [電路筆記工坊](https://mao0621.github.io/circuit-notes-hw9/) |
| AI 開發規則 | [AGENTS.md](AGENTS.md) |
| 如何持續新增內容 | [docs-authoring.md](docs-authoring.md) |

## 資料與安全

書籤保存在使用者自己的瀏覽器 `localStorage`，不會上傳到伺服器；清除瀏覽資料或更換裝置後不保證保留。若瀏覽器不允許儲存，閱讀功能仍可使用。

Repository 中不得放入 GitHub 權杖、API 金鑰、密碼、個人瀏覽器設定或其他人的資料。發布公開 Repository 前，應檢查待提交的檔案。開發與協作紀錄只記錄實際發生的對話、修改與檢查，不虛構 Gemini 回覆、截圖、測試結果或個人實驗經歷。

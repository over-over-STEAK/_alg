# 單字搜尋——Boyer–Moore 與動態規劃比較

## 1. 我在做什麼？

輸入一段文字 text 與關鍵字 pattern，找出關鍵字在文字中「所有出現的起始位置」。同一個問題分別使用動態規劃與非動態規劃解決。程式使用 Python 標準庫，不需要 pip 安裝套件。

例：banana 搜尋 ana，答案是 [1, 3]。位置從 0 開始，允許重疊；不是找出不連續的共同子序列。

## 2. 先照這樣操作（Windows）

1. 將 ZIP 完整解壓縮，不要在壓縮檔內直接執行。
2. 用 VS Code 的「開啟資料夾」開啟 week7。
3. 選「終端機 → 新增終端機」，確認終端機目前在 week7 資料夾。
4. 輸入以下指令（只輸入指令，不要複製 Markdown 的反引號）：

```powershell
py main.py
```

會自動展示四個範例。看到每組「結果一致：True」就是兩種演算法答案一致。

```text
文字： 'banana'
關鍵字： 'ana'
BM 結果： [1, 3]
DP 結果： [1, 3]
結果一致： True
```

接著執行測試與效能比較：

```powershell
py test_search.py
py benchmark.py
```

測試最後應顯示 OK。效能數字會受電腦與背景程式影響，不必與附檔完全相同。

若系統不認得 py，試試 python；兩者都不認得時，需先安裝 Python 3 並重新開啟終端機。建議 Python 3.10 以上。請以 UTF-8 儲存程式，避免中文編碼問題。

## 3. 自己換文字測試

```powershell
py main.py --text "banana" --pattern "ana"
py main.py --text "金門大學在金門" --pattern "金門"
py main.py --file examples/sample.txt --pattern "金門"
py BM.py "banana" "ana"
py DP.py "banana" "ana"
```

讀檔模式回傳整份文字的字元位置，不是行號；換行也占位置。使用 Python 文字模式讀檔，CRLF 會正規化為 LF。檔案模式會移除檔首 UTF-8 BOM。

## 4. 檔案用途

| 檔案 | 用途 |
|---|---|
| BM.py | Boyer–Moore：壞字元與強好後綴規則 |
| DP.py | 連續字串匹配的二維 DP |
| main.py | 自動展示、指定文字或讀取檔案 |
| test_search.py | 暴力法作為獨立基準，檢查兩個方法 |
| benchmark.py | 時間與 Python 記憶體配置比較 |
| benchmark_result.txt | 本次 AI 執行環境實測，不是學生本機紀錄 |
| REPORT.md | 演算法原理、複雜度、結果分析與個人紀錄欄位 |
| examples/sample.txt | UTF-8 測試文字 |

## 5. 統一規格

- 精確匹配且區分大小寫，不支援正規表示式。
- 回傳遞增排列的位置清單，從 0 開始，包含重疊匹配。
- 空關鍵字匹配每個文字邊界，例如 abc 搜尋空字串得到 [0,1,2,3]。
- 非空關鍵字比文字長或未出現時回傳 []。
- Python 字串以 Unicode 碼位為單位；不做 Unicode 正規化，一個畫面上的複合符號可能含多個碼位。
- 正式演算法不使用 str.find、正規表示式或外部搜尋套件。
- DP 版為方便教學保留完整表格，請先用小型文字測試，空間用量隨 n×m 成長。

## 6. 建議繳交內容

以老師實際規定為準，建議交完整 week7 資料夾或 ZIP、填寫身分資訊的報告，並附上自己的執行截圖：

1. py main.py：展示兩種方法結果一致。
2. py test_search.py：展示測試通過。
3. py benchmark.py：展示本機效能數據。

本專案由 AI 協助產生並在 AI 執行環境驗證。你仍需在自己的電腦執行、理解程式，依課程規範標示 AI 協助；不要將附檔數字寫成自己的本機實測。

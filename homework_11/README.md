# 第11週－數值方法與蒙地卡羅法

## AI 使用聲明
有使用 AI（ChatGPT）協助生成程式、測試及 Markdown 文件，並在 Python 環境執行測試。

## 題目與檔案

| 題目 | 程式 | 說明 |
|---|---|---|
| 1. 單變數微分與積分 | [q1_diff_int_1d.py](q1_diff_int_1d.py) | [q1_diff_int_1d.md](q1_diff_int_1d.md) |
| 2. 單變數蒙地卡羅積分 | [q2_mc_1d.py](q2_mc_1d.py) | [q2_mc_1d.md](q2_mc_1d.md) |
| 3. 多變數微分、最小值與超體積 | [q3_grad_integral_n.py](q3_grad_integral_n.py) | [q3_grad_integral_n.md](q3_grad_integral_n.md) |
| 4. 多變數蒙地卡羅積分 | [q4_mc_n.py](q4_mc_n.py) | [q4_mc_n.md](q4_mc_n.md) |
| 5. 通用 n 維黎曼積分 | [q5_riemann_n.py](q5_riemann_n.py) | [q5_riemann_n.md](q5_riemann_n.md) |
| 6. 通用 n 維蒙地卡羅積分 | [q6_mc_generic.py](q6_mc_generic.py) | [q6_mc_generic.md](q6_mc_generic.md) |

## 執行方式

Python 3，僅使用標準函式庫，不需安裝套件。

```bash
python -m unittest -v test_all

``
每題也可單獨執行。

## 理論值與比較

對 f(x)=Σxᵢ²，在 [0,1]ⁿ 上積分為 n/3，因每項的一維積分為 1/3，其餘維度長度皆為 1。

| 維度 | 理論值 | 黎曼格點數（每維10格） |
|---:|---:|---:|
|1|0.333333|10|
|2|0.666667|100|
|5|1.666667|100000|
|100|33.333333|10^100|

第5題的100維採用平方和可加分離性，等價化簡完整中點黎曼和，並非直接列舉，也不適用於任意函數。第6題使用一般蒙地卡羅抽樣，統計誤差通常隨樣本數以 1/√N 縮小（固定維度、有限變異數）。

## 參考資料

[課程：蒙地卡羅法](https://github.com/ccc115a/alg/blob/main/02-方法/09b-蒙地卡羅法/蒙地卡羅法.md)：介紹 Monte Carlo 與 Las Vegas 隨機演算法的差異。六題數值積分實作與測試為本專案另外撰寫。

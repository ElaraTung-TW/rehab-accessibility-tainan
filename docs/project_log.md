## 2026-08-12
### Environment Setup
- 在 VS Code 建立 Jupyter Notebook `01_population_exploration.ipynb`
- 使用 Python 3.14.3
- 安裝 pandas、NumPy
- 初次 import pandas 時遇到 NumPy DLL load error，確認 Terminal 可正常 import NumPy 後，重啟 Jupyter kernel 解決
### Concepts Learned
- `ModuleNotFoundError`：套件尚未安裝或目前環境找不到套件
- Notebook kernel 可能需要在安裝套件後重新啟動
- `os.getcwd()` 可確認 Python 的 current working directory
- 相對路徑是以 current working directory 為起點
- Notebook 位於 `notebooks/`，人口 CSV 位於 `data/raw/`。
- 相對路徑中的 `..` 代表回到上一層資料夾。
- 因此從 `notebooks/` 前往 `data/raw/` 的相對路徑為 `../data/raw/檔名.csv`。
### Today's Goal
* 定義復健資源與核心分析指標。
* 建立資料需求表。
* 找到並檢視第一份官方人口資料。
* 使用 Python / pandas 完成人口資料的初步清理與衍生指標計算。
### Research Design Progress
* 初步將復健資源區分為：
  * 醫院
  * 診所
  * 物理治療所
* 決定同時考慮：
  * Facility availability：各行政區復健服務機構數。
  * Workforce availability：各行政區執業物理治療師人數。
* 確認單純以機構家數或 PT 人數皆無法完全代表實際服務量，因此將實際治療量、治療模式與服務品質列為研究限制。
* MVP 的人口需求 proxy 暫定：
  * 總人口
  * 65 歲以上人口
* 車禍人數與外籍勞動人口暫列為延伸分析，不納入 MVP 核心指標。
* 本研究主要分析年度定為 2024 年（民國 113 年），以確保人口、物理治療師執業人數與醫療機構資料能盡可能使用相同年度與行政區層級。
  * 2025 年人口資料保留作為資料處理練習與後續更新用途，不作為目前主要分析基準。
### Data Requirements
目前確認需要：
* 各行政區總人口
* 各行政區 65+ 人口
* 各行政區執業 PT 人數
* 各行政區醫院數
* 各行政區診所數
* 各行政區物理治療所數
### Population Dataset
* 下載臺南市官方 2025 年 12 月人口 CSV。
* Raw file：
  `data/raw/population_age_tainan_2025_12.csv`
* 分析單位為臺南市各行政區。
* 原始資料包含：
  * 臺南市全市總計
  * 37 個行政區
  * 每個地理單位各有「計／男／女」三筆資料
### Population Data Cleaning Rules
* 分析總人口時僅保留 `性別 = 計`。
* 排除 `區域別 = 臺南市` 的全市總計列。
* 總人口使用 `總計` 欄位。
* 65+ 人口由下列年齡組加總：
  * 65–69
  * 70–74
  * 75–79
  * 80–84
  * 85–89
  * 90–94
  * 95–99
  * 100+
### Python / pandas Progress
建立：
`notebooks/01_population_exploration.ipynb`
學習與執行：
* `import pandas as pd`
* `os.getcwd()`：確認 current working directory。
* 相對路徑 `..`：代表回到上一層資料夾。
* `pd.read_csv()`：讀取 CSV。
* `df.head()`：查看前五筆資料。
* `df.shape`：確認資料列數與欄數。
* `value_counts()`：檢查類別出現次數。
* Boolean filtering：依條件篩選資料列。
* `.copy()`：建立獨立 DataFrame。
* 使用 column list 選取分析需要的欄位。
* `dtypes`：確認欄位資料型態。
* `.sum(axis=1)`：橫向加總多個年齡欄位。
* 建立新的衍生欄位。
### Data Validation
原始資料：
`114 rows × 125 columns`
確認：
* 38 個地理單位 × 計／男／女 = 114 rows。
* 僅保留「計」後：38 rows。
* 排除臺南市總計後：37 rows。
* 保留分析所需欄位後：37 rows × 10 columns。
* 所有人口欄位皆為整數型態。
* 確認所有行政區 `65+ population ≤ total population`。
* 肉眼檢查 37 個行政區結果，未發現明顯異常。
### Derived Variables
建立：
* `population_65_plus`
* `pct_65_plus`
計算：
`65+人口比例 = 65+人口 / 總人口 × 100`
### Output
完成 processed dataset：
`data/processed/population_tainan_2025_clean.csv`
### Troubleshooting
* 初次執行 `import pandas` 時出現 `ModuleNotFoundError`，確認 pandas 尚未安裝後使用 pip 安裝。
* 安裝後 Notebook 出現 NumPy DLL import error。
* Terminal 可正常載入 NumPy，因此判斷套件本身無問題。
* Restart Jupyter Kernel 後成功解決。
### Key Concepts Learned
* Raw data 原則上不直接修改。
* 在寫分析程式前先理解資料 schema。
* 資料讀入成功不代表資料一定正確，需進行 sanity check。
* Facility count、PT headcount 與 actual service capacity 是不同概念。
* 不同人口規模的行政區不能只比較絕對 PT 人數，後續需要人口標準化指標。
* Proxy 可以幫助測量無法直接觀察的概念，但必須清楚說明其限制。
### Next Step
下一次從「復健服務供給資料」開始：
1. 尋找可用的 PT 執業／醫事人員官方資料。
2. 尋找醫院、診所、物理治療所資料。
3. 檢查資料年份與行政區欄位是否能與人口資料匹配。
4. 確認後開始建立第二份 raw dataset。

## 2026-08-13
### Today's Goal
- 建立 2024 年臺南市復健服務供給端資料。
- 取得並整理物理治療師、復健科診所與復健科醫院資料。
- 確認物理治療所資料的可取得性。
### Reference Year Decision
原先暫定使用 2025 年資料，但衛福部鄉鎮市區層級的物理治療師執業人數目前可取得至 2024 年（民國 113 年）。
因此目前將主要分析年度調整為 2024 年，以盡量維持人口、醫事人力與醫療機構資料的年度一致性。
2025 年人口資料保留作為資料清理練習及後續更新用途。
### PT Workforce Data
Source:
- 衛福部「醫療院所現況－按鄉鎮市區別分」
- 指標：執業醫事人員數－物理治療師
- Year: 2024 (113年)
Processing:
- 從 Excel 原始表格擷取臺南市 37 個行政區。
- 保留行政區與物理治療師人數。
- 移除「臺南市」前綴。
- 將 PT 人數轉為 numeric。
- 檢查 missing values 與 duplicated districts。
Validation:
- 37 個行政區皆有資料。
- PT 人數合計 = 794，與官方臺南市總計一致。
- 16 個行政區的官方 PT 執業人數為 0。
Important:
目前只能解釋為「官方資料中該行政區 PT 執業人數為 0」，
不能直接推論該行政區完全沒有任何形式的復健服務。
Output:
- data/processed/pt_workforce_tainan_2024_clean.csv
### Rehabilitation Clinic Data
Source:
- 113年診所科別統計
Raw data structure:
- Wide format
- 一列代表一個鄉鎮市區
- 專科別（例如復健科）分別為不同欄位
Processing:
- 使用鄉鎮市區碼 501–538 篩選臺南市資料。
- 使用官方欄位說明中的行政區 codebook。
- 透過 pandas merge，以「鄉鎮市區碼」將行政區名稱加入主資料。
- 保留 district 與 rehab_clinic_count。
Validation:
- 37 個行政區。
- Merge 後無 missing district。
- 無 duplicated district。
- 復健科欄位無 missing value。
- 0 代表官方統計家數為 0，與 NaN（資料缺失）意義不同。
Output:
- data/processed/rehab_clinics_tainan_2024_clean.csv
### Rehabilitation Hospital Data
Source:
- 113年醫院科別統計
Initial observation:
以鄉鎮市區碼 501–538 篩選後只有 13 個行政區，而不是預期的 37 區。
Investigation:
- 檢查這 13 筆資料後，確認其「醫院家數」皆大於 0。
- 因此判斷醫院資料採 sparse format：只有實際存在醫院的行政區才會出現在資料中。
Processing decision:
不能直接以醫院資料作為 left table，否則沒有醫院的行政區會消失。
改以完整的 37 區行政區 codebook 作為 left table，再與醫院資料 merge。
對於原始資料中沒有出現的行政區：
- 已確認其原因為該區沒有醫院。
- 因此「設有復健科的醫院數」可合理補為 0。
Important lesson:
不能看到 NaN 就直接 fillna(0)。
必須先確認 missing value 的形成原因，才能決定是否能合理視為 0。
Output:
- data/processed/rehab_hospitals_tainan_2024_clean.csv
### Physical Therapy Clinic Data Gap
物理治療所是本研究重要的復健服務供給來源，但目前尚未確認可與其他 2024 年資料維持相同時間點與行政區層級的歷史資料。
現有「醫療機構與人員基本資料」屬持續更新資料，可能與年度統計資料存在時間點與統計口徑差異。
因此目前不為了補齊 facility types 而直接混用不同時間點資料。
下一階段：
- 確認是否有可取得的 2024 年物理治療所歷史資料。
- 若無法取得，需明確記錄為 data availability constraint / research limitation。
### Key Concepts Learned
- pandas merge 與 SQL JOIN 的核心概念相同。
- 使用 left join 可以保留分析所需的完整行政區。
- Merge 後必須檢查 row count、missing values 與 duplicated keys。
- 0 與 missing value (NaN) 的研究意義不同。
- 不同官方資料集即使主題相似，也可能採不同資料結構。
- Sparse data 必須先理解缺列原因，再決定如何處理。
- 年度一致性比單純「把所有資料湊齊」更重要。
### Next Step
1. 將人口資料改用 2024 年並重跑既有 cleaning pipeline。
2. 確認物理治療所的 2024 歷史資料來源。
3. 檢查所有 processed datasets 的行政區名稱是否完全一致。
4. 建立第一版 master table。
5. 計算 PT per 10,000 population 等核心指標。

## 2026-08-27
### Today's Goal
- 複習既有資料清理流程。
- 將人口資料由 2025 更新為 2024。
- 對所有 processed datasets 進行 merge 前 QC。
- 建立第一版 master table。

### Population Data - 2024
重新使用既有 population cleaning pipeline 處理 2024 年資料。
Data quality issue:
- 2024 年原始人口 CSV 與 2025 年 schema 不完全相同。
- 原始資料包含異常欄位名稱 `歲人數` 與 `歲人數以上`。
- 因此不直接使用異常欄位計算 65+ 人口。

Alternative calculation:
- 先加總 0–64 歲人口。
- population_65_plus = total_population - population_under_65

Validation:
- 將 population_65_plus 與 65–99 歲人口加總比較。
- 反推出 implied 100+ population。
- 各行政區結果皆為合理的非負小數量。
- 37 區 implied 100+ 加總與臺南市總計一致。

Final variables:
- district
- total_population
- population_65_plus
- pct_65_plus

Output:
- data/processed/population_tainan_2024_clean.csv

### Merge Preparation / QC
目前四份 processed datasets：
- population_tainan_2024_clean.csv
- pt_workforce_tainan_2024_clean.csv
- rehab_clinics_tainan_2024_clean.csv
- rehab_hospitals_tainan_2024_clean.csv

QC results:
- 四份資料皆為 37 個行政區。
- district key 無 missing values。
- district key 無 duplicates。
- 行政區名稱可作為共同 merge key。

### Master Table v1
以 population dataset 作為主表，透過 district 進行 left merge：
population
+ PT workforce
+ rehabilitation clinics
+ rehabilitation hospitals

Final columns:
- district
- total_population
- population_65_plus
- pct_65_plus
- pt_count
- rehab_clinic_count
- rehab_hospital_count

Validation:
- Shape = (37, 7)
- No missing values
- No duplicated districts

Output:
- data/processed/master_table_tainan_2024_v1.csv

### Key Concepts Reviewed
- Load → Inspect → Filter → Transform → Validate → Merge → Export
- pandas merge 與 SQL JOIN 的概念
- merge 前應先檢查 key 的 missing、duplicate 與命名一致性
- NaN 不能在不了解原因時直接填 0
- 不同年度官方資料可能有不同 schema
- cleaning pipeline 的邏輯可以重用，但不能假設欄位名稱完全相同
- Notebook 應能在 Restart Kernel 後 Run All 成功

### Next Step
- 從 master_table_tainan_2024_v1.csv 開始正式分析。
- 計算 PT per 10,000 population。
- 計算與 65+ population 相關的供需指標。
- 建立第一批 ranking 與簡單視覺化。

## 2026-09-02
- Calculated the first accessibility indicator: PT per 10,000 population.
- Several districts showed pt_per_10000 = 0 because the official 2024 PT workforce count was 0.
- These results indicate potential workforce gaps, but should not be interpreted as absence of all rehabilitation services.
- Next step: compare PT workforce with rehabilitation clinics, hospitals, and older-population indicators.
- 部分臺南市行政區在官方資料中呈現零登記物理治療師的情形，顯示可能存在明顯的復健人力供給缺口，但仍需結合醫療機構分布與其他服務型態進一步判讀。

## 2026-09-20

### Project MVP Completed

- Finalized core accessibility indicators.
- Created three project visualizations.
- Completed a Streamlit prototype dashboard.
- Added data limitations and district-level summary.
- Completed project README and GitHub repository.
- Deployed the dashboard publicly using Streamlit Community Cloud.

### Live Dashboard
https://rehab-accessibility-tainan.streamlit.app/

### Current Status
The graduate application MVP is complete.

The project is intentionally frozen at the current scope. Future extensions may include:
- physical therapy clinic data
- travel-time accessibility
- actual service utilization
- additional demand indicators
- SQL-based analysis

These extensions are not required for the current graduate application version.
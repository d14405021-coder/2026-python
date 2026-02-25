# 2026 Python CPE Weekly Practice

以開源專案常見結構整理每週課程與解題進度，方便協作、版本控管與後續擴充。

## 🎯 快速開始

**首次使用？** 👉 閱讀 [`docs/analysis/FINAL_SUMMARY.md`](docs/analysis/FINAL_SUMMARY.md) 了解項目現況與優先級建議（15 分鐘）

## 📁 目錄結構

```
.
├── docs/
│   ├── COURSE_PLAN.md              # 課程計劃表
│   └── analysis/                   # 📊 分析與報告（新增）
│       ├── README.md               # 分析文件導覽
│       ├── FINAL_SUMMARY.md        # 完整驗證報告（⭐ 從這裡開始）
│       ├── VERIFICATION_REPORT.md  # 優先級建議
│       ├── ANALYSIS_REPORT.md      # 課程分析
│       ├── questions_analysis.json # 結構化資料
│       ├── questions_analysis.csv  # Excel 匯入格式
│       └── ... (其他分析檔案)
├── weeks/
│   ├── week-01/ ~ week-13/
│   │   ├── README.md
│   │   ├── QUESTION-*.md
│   │   └── solutions/
├── .gitignore
└── README.md (本檔案)
```

## 📚 使用說明

### 課程組織
- 每週資料放在 `weeks/week-XX/` 目錄
- 題目說明檔 `weeks/week-XX/QUESTION-*.md`
- 解題代碼放在各週的 `solutions/` 子目錄
- 每週概覽放在各週 `README.md`

### 查看分析與報告
進入 [`docs/analysis/`](docs/analysis/) 目錄查看：
- **FINAL_SUMMARY.md** - 完整驗證報告與優先級建議（推薦首先閱讀）
- **CLASSIFICATION_TABLE.txt** - 所有 49 題的分類清單
- **questions_analysis.json/csv** - 結構化資料（資料分析或系統整合用）

更詳細的導覽和使用方式，請參考 [`docs/analysis/README.md`](docs/analysis/README.md)

### 題號參考
題目來源與題解：<https://yuihuang.com/cpe-level-1/>
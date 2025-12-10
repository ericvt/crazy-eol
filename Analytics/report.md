# Data Analysis Report

---

## Analysis #1: Unique Counts and Combinations

### A) Unique Counts

| Dimension | Count |
|-----------|-------|
| Unique Tenants | 41 |
| Unique Branches | 310 |
| Unique Content Group Categories | 11 |
| Unique Cultures | 59 |
| Unique Translation Flavors | 5 |

### B) Combinations

| Metric | Count |
|--------|-------|
| Branch to Content Group Category Combinations | 956 |
| Culture Groupings | 58 |

### C) Culture Grouping Statistics

| Metric | Value |
|--------|-------|
| Minimum cultures in a grouping | 1 |
| Maximum cultures in a grouping | 55 |
| Average cultures per grouping | 14.5 |

---

## Analysis #2: Relationship Between Content Group Categories and Translation Flavors

| Content Group Category | AIPE | HPE | HT | MT | MTPE | Total |
|------------------------|------|-----|----|----|------|-------|
| SelfServe_Art | 0 | 0 | 7 | 0 | 0 | 7 |
| SelfServe_CaD | 6 | 0 | 0 | 12 | 2 | 20 |
| SelfServe_Conceptual | 293 | 68 | 0 | 147 | 0 | 508 |
| SelfServe_Legal | 4 | 0 | 1 | 0 | 20 | 25 |
| SelfServe_MD | 0 | 1 | 0 | 1 | 0 | 2 |
| SelfServe_Reference_Authored | 12 | 6 | 0 | 315 | 0 | 333 |
| SelfServe_Reference_Managed | 12 | 7 | 0 | 314 | 0 | 333 |
| SelfServe_Resjson | 0 | 0 | 0 | 1 | 0 | 1 |
| SelfServe_Training | 18 | 15 | 0 | 15 | 0 | 48 |
| SelfServe_Video | 4 | 0 | 0 | 4 | 0 | 8 |
| SelfServe_YML | 6 | 7 | 0 | 8 | 1 | 22 |
| **Total** | **355** | **104** | **8** | **817** | **23** | **1307** |

---

## Analysis #3: Locale Support by Translation Flavor

### A) MT Translation Flavor

MT supported locales: 57

ar-SA, bg-BG, bs-Latn-BA, ca-ES, cs-CZ, da-DK, de-AT, de-CH, de-DE, el-GR, es-ES, es-MX, et-EE, eu-ES, fi-FI, fil-PH, fr-BE, fr-CA, fr-CH, fr-FR, ga-IE, gl-ES, he-IL, hi-IN, hr-HR, hu-HU, id-ID, is-IS, it-CH, it-IT, ja-JP, ka-GE, kk-KZ, ko-KR, lt-LT, lv-LV, ms-MY, mt-MT, nb-NO, nl-BE, nl-NL, pl-PL, pt-BR, pt-PT, ro-RO, ru-RU, sk-SK, sl-SI, sr-Cyrl-RS, sr-Latn-RS, sv-SE, th-TH, tr-TR, uk-UA, vi-VN, zh-CN, zh-TW

MT non-supported locales: 2

lb-LU, zh-HK

### B) AIPE Translation Flavor

AIPE supported locales: 25

ar-SA, cs-CZ, da-DK, de-DE, el-GR, es-ES, fi-FI, fr-FR, he-IL, hu-HU, id-ID, it-IT, ja-JP, ko-KR, nb-NO, nl-NL, pl-PL, pt-BR, pt-PT, ru-RU, sv-SE, th-TH, tr-TR, zh-CN, zh-TW

AIPE non-supported locales: 34

bg-BG, bs-Latn-BA, ca-ES, de-AT, de-CH, es-MX, et-EE, eu-ES, fil-PH, fr-BE, fr-CA, fr-CH, ga-IE, gl-ES, hi-IN, hr-HR, is-IS, it-CH, ka-GE, kk-KZ, lb-LU, lt-LT, lv-LV, ms-MY, mt-MT, nl-BE, ro-RO, sk-SK, sl-SI, sr-Cyrl-RS, sr-Latn-RS, uk-UA, vi-VN, zh-HK

---

## Analysis #4: Branch MT Culture Coverage

**Question:** Is there any branch where translation flavor = MT that does not match the full culture list from 'MT supported locales'? (Are we missing MT supported cultures for those branches?)

**Answer:** YES

- **Total branches with MT:** 304
- **Branches missing some MT cultures:** 302 (99.3%)
- **Branches with complete MT coverage:** 2 (0.7%)

Most branches with MT translation flavor are missing some of the 57 MT supported locales. Coverage ranges from 1.8% (1 out of 57 locales) to 100% (all 57 locales).

Lowest Coverage Branches:

- github-docs-internal.main: 1.8% (1/57)
- mc-docs-pr.main: 1.8% (1/57)
- mc-docs-pr.live: 1.8% (1/57)
- azure-china-pr.live: 1.8% (1/57)

---

## Analysis #5: Most Common Culture

Most common culture: fr-FR

Occurrences: 952

### a) Unique branches including fr-FR

- Count: 306
- Percentage: 98.71% of 310 total branches

### b) Unique branches NOT including fr-FR

- Count: 4
- Percentage: 1.29% of 310 total branches

---

*Report Generated from data_processed.csv*

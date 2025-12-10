# Content EOL Viewer

Interactive visualization of translation flavors across Content tenants, branches and culture groups.

## 🌐 View Pages

Matrix showing **Tenants and associated Culture Groups**. Displays also the number of branches and their quality level:
[tenant_culturegroup.html](https://growth-ecosystems.github.io/crazy-eol/local/tenant_culturegroup.html)

Table showing the **Translation Flavor distribution for Tenants and Branches**
[tenant_branch_transflavors.html](https://growth-ecosystems.github.io/crazy-eol/local/tenant_branch_TransFlavors.html)

Table showing **Cultures and Translation Flavors for each Branch**
[branch_culture.html](https://growth-ecosystems.github.io/crazy-eol/local/branch_culture.html)


## 🔄 Data Pipeline

data.csv is the output from the Jupiter Tenant and Branch Config PBI report

> ⚠️ **Note:** data.csv is not automatically generated, so the current version on this repo may be outdated.

### Transform Raw Data
`transform_data.py` script processes `data.csv` through 4 automated steps:

1. **Sort Cultures** - Alphabetically sorts culture codes within each branch
2. **Apply Translation Flavor** - Assigns flavor based on QE/AIPE and HPE flags
3. **Create Pivot Table** - Aggregates data by tenant and culture group
4. **Generate Viewer** - Creates self-contained HTML with embedded data

### Translation Flavor Logic

- **Preserve existing values** - Pre-existing flavors (HT, MTPE) are never overwritten
- **Translation Provider Type = CtsDownstreamConnectorSagaTemplate + QE=FALSE** → MT
- **QE=TRUE + HPE=TRUE** → HPE
- **QE=TRUE + HPE=FALSE** → AIPE
- **QE=TRUE + HPE=blank** → AIPE
- **QE=FALSE + HPE=TRUE** → HPE
- **QE=FALSE + HPE=FALSE** → MT
- **Both blank** → Keep existing (warns if also blank)

## 🎨 Translation Flavors

| Flavor | Name | Color |
|--------|------|-------|
| **MT** | Machine Translation | Red |
| **AIPE** | AI Post-Edit | Yellow |
| **MTPE** | MT Post-Edit | Light Brown |
| **HPE** | Human Post-Edit | Light Green |
| **HT** | Human Translation | Dark Green |

## 📂 Files

**Source:**
- `data.csv` - Input data file

**Scripts:**
- `transform_data.py` - Main processing pipeline
- `start_server.sh` - Local development server

**Generated:**
- `data_processed.csv` - Processed source data with Translation Flavor logic applied
- `data_pivot.csv` - Pivot table data

**HTML Viewers (in `local/` folder):**
- `tenant_branch_TransFlavors.html` - Tenant-Branch Translation Flavors view
- `branch_culture.html` - Content Branch-Culture view
- `tenant_culturegroup.html` - Content Tenant-Culture Group Associations view

## 🛠️ Run-it locally

To view the pages locally, run:

```bash
./start_server.sh
```

Then open your browser to:
- http://localhost:8000/local/tenant_branch_TransFlavors.html
- http://localhost:8000/local/branch_culture.html
- http://localhost:8000/local/tenant_culturegroup.html


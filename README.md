# EOL Translation Pivot Table

Interactive visualization of translation flavors across tenants and culture groups.

## 🌐 View Online

Visit: https://ericvt.github.io/crazy-eol/pivot_viewer_embedded.html

## 📋 Quick Start

Process the data and generate all output files:

```bash
python3 process_pipeline.py
```

View the results locally:

```bash
python3 start_viewer.py
```

## 🔄 Data Pipeline

The `process_pipeline.py` script processes `data.csv` through 4 automated steps:

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
- `process_pipeline.py` - Main processing pipeline
- `start_viewer.py` - Local development server

**Generated:**
- `data_processed.csv` - Processed source data with Translation Flavor logic applied
- `data_pivot.csv` - Pivot table data
- `pivot_viewer_embedded.html` - Self-contained interactive viewer
- `pivot_viewer.html` - Viewer template (requires server)

## 🚀 Deployment

The `pivot_viewer_embedded.html` file is self-contained and can be:
- Opened directly in any web browser
- Hosted on GitHub Pages
- Shared without requiring data files or a web server

## 🛠️ Development

To modify the visualization, edit `pivot_viewer.html` and regenerate:

```bash
python3 process_pipeline.py
```

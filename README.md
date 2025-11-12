# EOL Translation Pivot Table

Interactive visualization of translation flavors across tenants and culture groups.

## View Online

Visit: [Your GitHub Pages URL will be here]

## Files

- `pivot_viewer_embedded.html` - Self-contained interactive viewer
- `tenant_culture_group_pivot.csv` - Pivot table data
- `data_sorted_cultures.csv` - Source data

## Translation Flavors

- **MT** (Machine Translation) - Red
- **AIPE** (AI Post-Edit) - Purple
- **MTPE** (MT Post-Edit) - Yellow
- **HPE** (Human Post-Edit) - Light Green
- **HT** (Human Translation) - Dark Green

## Local Development

To regenerate the data:

```bash
python3 update_translation_flavor.py  # Update flavors in source data
python3 create_pivot_final.py         # Generate pivot table
python3 create_embedded_viewer.py     # Create embedded viewer
python3 start_viewer.py                # Start local server
```

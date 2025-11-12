"""
Creates a self-contained HTML viewer with embedded CSV data
"""
import csv

# Read the CSV data
csv_data = []
with open('tenant_culture_group_pivot.csv', 'r', encoding='utf-8') as f:
    csv_data = f.read()

# Read the HTML template
with open('pivot_viewer.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find where to inject the data - look for the loadDefaultData function
# We'll replace the fetch call with embedded data

embedded_js = f'''
        function loadDefaultData() {{
            const csvData = `{csv_data}`;
            parseCSV(csvData);
        }}
'''

# Replace the loadDefaultData function
import re
pattern = r'function loadDefaultData\(\) \{[^}]*fetch\([^}]*\}[^}]*\}[^}]*\}'
replacement = embedded_js.strip()

html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Write the new self-contained HTML
with open('pivot_viewer_embedded.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Created pivot_viewer_embedded.html")
print("📄 This file contains all data embedded and works without a web server")
print("🌐 Perfect for GitHub Pages or opening directly in a browser")

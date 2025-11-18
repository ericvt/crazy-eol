#!/usr/bin/env python3
"""
EOL Translation Data Processing Pipeline

Processes data.csv through the complete workflow:
1. Sort cultures alphabetically
2. Populate blank Culture Groups
3. Apply translation flavor logic
4. Generate pivot table
5. Create embedded HTML viewer

Usage: python3 process_pipeline.py
"""

import csv
import re
from collections import defaultdict

print("="*80)
print("EOL TRANSLATION DATA PROCESSING PIPELINE")
print("="*80)

# ============================================================================
# STEP 1: SORT CULTURES ALPHABETICALLY
# ============================================================================
print("\n[STEP 1/5] Sorting cultures alphabetically...")
print("-"*80)

with open('data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

sorted_count = 0
for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    if cultures:
        # Split by comma, strip whitespace, sort, and rejoin
        culture_list = [c.strip() for c in cultures.split(',')]
        sorted_cultures = ','.join(sorted(culture_list))
        
        if sorted_cultures != cultures:
            row['Cultures'] = sorted_cultures
            sorted_count += 1

# Write sorted data to intermediate file
with open('data_sorted_cultures.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Sorted cultures in {sorted_count} rows")
print(f"   Output: data_sorted_cultures.csv ({len(rows)} rows)")


# ============================================================================
# STEP 2: POPULATE BLANK CULTURE GROUPS
# ============================================================================
print("\n[STEP 2/5] Populating blank Culture Groups...")
print("-"*80)

# Read the sorted data
with open('data_sorted_cultures.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Group rows by tenant for efficient matching
tenant_data = defaultdict(list)
for row in rows:
    tenant = row.get('Tenant', '').strip()
    if tenant:
        tenant_data[tenant].append(row)

# Track statistics
blank_count = 0
matched_same_tenant_count = 0
matched_other_tenant_count = 0
defaulted_count = 0
matched_details = []

# Process each row to populate blank Culture Groups
for row in rows:
    culture_group = row.get('Culture Group', '').strip()
    
    if not culture_group:  # Culture Group is blank
        blank_count += 1
        tenant = row.get('Tenant', '').strip()
        branch = row.get('Branch', '').strip()
        cultures = row.get('Cultures', '').strip('"')
        
        # Sort cultures for comparison
        cultures_sorted = ','.join(sorted([c.strip() for c in cultures.split(',')])) if cultures else ''
        
        # STEP 1: Search for matching cultures in OTHER branches of the same tenant
        match_found = False
        for other_row in tenant_data[tenant]:
            if other_row['Branch'] != branch:  # Don't match with same branch
                other_cultures = other_row.get('Cultures', '').strip('"')
                other_cultures_sorted = ','.join(sorted([c.strip() for c in other_cultures.split(',')])) if other_cultures else ''
                other_culture_group = other_row.get('Culture Group', '').strip()
                
                if cultures_sorted == other_cultures_sorted and other_culture_group:
                    # Match found within same tenant!
                    row['Culture Group'] = other_culture_group
                    matched_same_tenant_count += 1
                    matched_details.append(f"  • Branch '{branch[:40]}' → '{other_culture_group}' (same tenant: '{other_row['Branch'][:40]}')")
                    match_found = True
                    break
        
        # STEP 2: If no match in same tenant, search across ALL other tenants
        if not match_found:
            for other_tenant, other_tenant_rows in tenant_data.items():
                if other_tenant != tenant:  # Different tenant
                    for other_row in other_tenant_rows:
                        other_cultures = other_row.get('Cultures', '').strip('"')
                        other_cultures_sorted = ','.join(sorted([c.strip() for c in other_cultures.split(',')])) if other_cultures else ''
                        other_culture_group = other_row.get('Culture Group', '').strip()
                        
                        if cultures_sorted == other_cultures_sorted and other_culture_group:
                            # Match found in different tenant!
                            row['Culture Group'] = other_culture_group
                            matched_other_tenant_count += 1
                            matched_details.append(f"  • Branch '{branch[:40]}' → '{other_culture_group}' (other tenant: {other_tenant})")
                            match_found = True
                            break
                    if match_found:
                        break
        
        # STEP 3: If still no match found, apply default: Translation Provider Name + '_' + culture count
        if not match_found:
            provider_name = row.get('Translation Provider Name', '').strip()
            culture_count = len(cultures.split(',')) if cultures else 0
            default_culture_group = f"{provider_name}_{culture_count}"
            row['Culture Group'] = default_culture_group
            defaulted_count += 1

# Write updated data
with open('data_sorted_cultures.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Culture Group population completed")
print(f"   Total blank Culture Groups found: {blank_count}")
print(f"   Matched from same tenant: {matched_same_tenant_count}")
print(f"   Matched from other tenants: {matched_other_tenant_count}")
print(f"   Set to default value: {defaulted_count}")

if matched_details:
    print(f"\n   Matched branches:")
    for detail in matched_details[:10]:  # Show first 10
        print(detail)
    if len(matched_details) > 10:
        print(f"   ... and {len(matched_details) - 10} more")

# Verification: Check if any Culture Groups are still blank
still_blank = sum(1 for row in rows if not row.get('Culture Group', '').strip())
if still_blank > 0:
    print(f"\n   ⚠️  WARNING: {still_blank} rows still have blank Culture Groups!")
else:
    print(f"\n   ✅ VERIFICATION: All rows now have Culture Groups assigned")


# ============================================================================
# STEP 3: APPLY TRANSLATION FLAVOR LOGIC
# ============================================================================
print("\n[STEP 3/5] Applying Translation Flavor logic...")
print("-"*80)

warnings = []
qe_true_hpe_blank_count = 0
flavor_rows = []

with open('data_sorted_cultures.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    row_num = 1  # Start at 1 for header
    
    for row in reader:
        row_num += 1
        qe_enabled = row.get('QE/AIPE Enabled', '').strip().upper()
        hpe_enabled = row.get('HPE Enabled', '').strip().upper()
        current_flavor = row.get('TranslationFlavor', '').strip()
        provider_type = row.get('Translation Provider Type', '').strip()
        provider_type = row.get('Translation Provider Type', '').strip()
        
        # Rule: Preserve original TranslationFlavor if not blank
        if current_flavor:
            # Keep existing flavor, don't overwrite
            flavor_rows.append(row)
            continue
        
        # Apply Translation Flavor logic only when TranslationFlavor is blank
        # Rule: Translation Provider Type = CtsDownstreamConnectorSagaTemplate + QE=FALSE → MT
        if provider_type == 'CtsDownstreamConnectorSagaTemplate' and qe_enabled == 'FALSE':
            row['TranslationFlavor'] = 'MT'
        # Rule #2: QE=TRUE + HPE=blank → AIPE
        elif qe_enabled == 'TRUE' and hpe_enabled == '':
            row['TranslationFlavor'] = 'AIPE'
            qe_true_hpe_blank_count += 1
            warnings.append(f"Row {row_num}: QE=TRUE, HPE=blank → Set to AIPE (Tenant: {row.get('Tenant', '')[:30]}, Branch: {row.get('Branch', '')[:30]})")
        # QE=TRUE + HPE=TRUE → HPE
        elif qe_enabled == 'TRUE' and hpe_enabled == 'TRUE':
            row['TranslationFlavor'] = 'HPE'
        # QE=TRUE + HPE=FALSE → AIPE
        elif qe_enabled == 'TRUE' and hpe_enabled == 'FALSE':
            row['TranslationFlavor'] = 'AIPE'
        # QE=FALSE + HPE=TRUE → HPE
        elif qe_enabled == 'FALSE' and hpe_enabled == 'TRUE':
            row['TranslationFlavor'] = 'HPE'
        # QE=FALSE + HPE=FALSE → MT
        elif qe_enabled == 'FALSE' and hpe_enabled == 'FALSE':
            row['TranslationFlavor'] = 'MT'
        # Rule #1: Both QE and HPE blank → Keep existing (should have pre-existing flavor)
        elif qe_enabled == '' and hpe_enabled == '':
            # TranslationFlavor should have a pre-existing value, but it's blank
            row['TranslationFlavor'] = ''
            warnings.append(f"⚠️  Row {row_num}: Both QE/AIPE and HPE are blank, but TranslationFlavor is also blank (Tenant: {row.get('Tenant', '')[:30]}, Branch: {row.get('Branch', '')[:30]})")
        else:
            # Other cases (e.g., QE=FALSE and HPE=blank) - keep blank
            row['TranslationFlavor'] = ''
        
        flavor_rows.append(row)

# Write updated data back
with open('data_sorted_cultures.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(flavor_rows)

# Calculate flavor distribution
flavor_counts = {}
for row in flavor_rows:
    flavor = row['TranslationFlavor']
    flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1

print(f"✅ Translation Flavor applied to {len(flavor_rows)} rows")
if qe_true_hpe_blank_count > 0:
    print(f"   ℹ️  {qe_true_hpe_blank_count} rows had QE=TRUE with HPE=blank, set to AIPE")
if warnings:
    print(f"   ⚠️  {len(warnings)} rows with blank QE/HPE/TranslationFlavor (likely footer rows)")

print(f"\n   Flavor Distribution:")
for flavor, count in sorted(flavor_counts.items()):
    if flavor:
        print(f"      {flavor}: {count}")


# ============================================================================
# STEP 4: CREATE PIVOT TABLE
# ============================================================================
print("\n[STEP 4/5] Creating pivot table...")
print("-"*80)

branch_counts = defaultdict(lambda: defaultdict(set))
branch_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
culture_group_cultures = {}
all_culture_groups = set()
all_tenants = set()
all_branches = set()  # Track all unique branches

with open('data_sorted_cultures.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        tenant = row.get('Tenant', '').strip()
        culture_group = row.get('Culture Group', '').strip()
        branch = row.get('Branch', '').strip()
        cultures = row.get('Cultures', '').strip()
        translation_flavor = row.get('TranslationFlavor', '').strip()
        qe_enabled = row.get('QE/AIPE Enabled', '').strip()
        hpe_enabled = row.get('HPE Enabled', '').strip()
        
        if tenant and culture_group and branch:
            branch_counts[tenant][culture_group].add(branch)
            all_culture_groups.add(culture_group)
            all_tenants.add(tenant)
            all_branches.add(branch)  # Track unique branch
            
            # Store metadata for this combination
            branch_metadata[tenant][culture_group][branch] = {
                'flavor': translation_flavor,
                'qe': qe_enabled,
                'hpe': hpe_enabled
            }
            
            # Store the cultures for this culture group (if not already stored)
            if culture_group not in culture_group_cultures and cultures:
                culture_group_cultures[culture_group] = cultures

# Sort tenants alphabetically
sorted_tenants = sorted(all_tenants)

# Sort culture groups by actual number of cultures (least to highest)
def get_culture_count(culture_group):
    cultures = culture_group_cultures.get(culture_group, '')
    return len(cultures.split(',')) if cultures else 0

sorted_culture_groups = sorted(all_culture_groups, key=get_culture_count)

# Write pivot table to CSV
with open('data_pivot.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Metadata row (will be parsed by JavaScript)
    metadata = ['# METADATA', f'TOTAL_BRANCHES={len(all_branches)}', '', ''] + [''] * len(sorted_tenants)
    writer.writerow(metadata)
    
    # Header row
    header = ['Culture Group', 'Number of Cultures', 'Cultures'] + sorted_tenants
    writer.writerow(header)
    
    # Data rows
    for culture_group in sorted_culture_groups:
        cultures = culture_group_cultures.get(culture_group, '')
        count = len(cultures.split(',')) if cultures else 0
        
        row = [culture_group, count, cultures]
        
        # Add branch counts and metadata for each tenant
        for tenant in sorted_tenants:
            branches = branch_counts[tenant][culture_group]
            branch_count = len(branches)
            
            if branch_count > 0:
                # Determine the predominant flavor/settings
                flavors = []
                qe_true_hpe_false = 0
                qe_true_hpe_true = 0
                
                for branch in branches:
                    meta = branch_metadata[tenant][culture_group][branch]
                    flavors.append(meta['flavor'])
                    if meta['qe'].upper() == 'TRUE':
                        if meta['hpe'].upper() == 'TRUE':
                            qe_true_hpe_true += 1
                        else:
                            qe_true_hpe_false += 1
                
                # Determine predominant flavor
                flavor_counts_cell = {}
                for f in flavors:
                    if f:
                        flavor_counts_cell[f] = flavor_counts_cell.get(f, 0) + 1
                
                predominant_flavor = max(flavor_counts_cell.items(), key=lambda x: x[1])[0] if flavor_counts_cell else ''
                
                # Format: count|flavor|qe_hpe_false|qe_hpe_true
                cell_value = f"{branch_count}|{predominant_flavor}|{qe_true_hpe_false}|{qe_true_hpe_true}"
                row.append(cell_value)
            else:
                row.append('')
        
        writer.writerow(row)

print(f"✅ Pivot table created")
print(f"   Dimensions: {len(sorted_tenants)} tenants × {len(sorted_culture_groups)} culture groups")
print(f"   Output: data_pivot.csv")


# ============================================================================
# STEP 5: CREATE EMBEDDED HTML VIEWER
# ============================================================================
print("\n[STEP 5/5] Creating embedded HTML viewer...")
print("-"*80)

# Read the CSV data
with open('data_pivot.csv', 'r', encoding='utf-8') as f:
    csv_data = f.read()

# Read the HTML template
with open('pivot_viewer.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Create embedded JavaScript that replaces the async loadCSV function
# We'll replace it with a synchronous version that uses embedded data
embedded_load_function = f'''
        // Load and parse CSV (embedded data version)
        async function loadCSV() {{
            const text = `{csv_data}`;
            parseCSV(text);
            // Note: Original data loading skipped for embedded version
            return;
        }}'''

# Replace the loadCSV function
pattern = r'// Load and parse CSV\s+async function loadCSV\(\) \{[^}]*\{[^}]*\}[^}]*\}[^}]*\}'
html_content = re.sub(pattern, embedded_load_function.strip(), html_content, flags=re.DOTALL)

# Write the self-contained HTML
with open('pivot_viewer_embedded.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Embedded viewer created")
print(f"   Output: pivot_viewer_embedded.html")


# ============================================================================
# CLEANUP TEMPORARY FILES
# ============================================================================
print("\n[CLEANUP] Saving final processed data and removing temporary files...")
print("-"*80)

import os

# Save the processed data with a final name before cleanup
if os.path.exists('data_sorted_cultures.csv'):
    import shutil
    shutil.copy('data_sorted_cultures.csv', 'data_processed.csv')
    print(f"✅ Saved: data_processed.csv (source data with Translation Flavor applied)")
    os.remove('data_sorted_cultures.csv')
    print(f"✅ Deleted temporary: data_sorted_cultures.csv")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
print("="*80)
print("\nGenerated files:")
print("  📄 data_processed.csv - Source data with Translation Flavor logic applied")
print("  📊 data_pivot.csv - Pivot table data")
print("  🌐 pivot_viewer_embedded.html - Self-contained interactive viewer")
print("\nNext steps:")
print("  • View locally: python3 start_viewer.py")
print("  • Deploy: Push pivot_viewer_embedded.html to GitHub Pages")
print("="*80)

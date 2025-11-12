import csv
from collections import defaultdict

# Read the CSV with sorted cultures
with open('data_sorted_cultures.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Build pivot data: tenant -> culture_group -> set of branches
pivot_data = defaultdict(lambda: defaultdict(set))
all_culture_groups = set()
all_tenants = set()

for row in rows:
    tenant = row.get('Tenant', '').strip()
    culture_group = row.get('Culture Group', '').strip()
    branch = row.get('Branch', '').strip()
    
    if tenant and culture_group and branch:
        pivot_data[tenant][culture_group].add(branch)
        all_culture_groups.add(culture_group)
        all_tenants.add(tenant)

# Sort tenants and culture groups
sorted_tenants = sorted(all_tenants)
sorted_culture_groups = sorted(all_culture_groups)

# Write to CSV file for Excel/spreadsheet import
output_file = 'tenant_culture_group_pivot.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Header row
    header = ['Tenant'] + sorted_culture_groups
    writer.writerow(header)
    
    # Data rows
    for tenant in sorted_tenants:
        row_data = [tenant]
        for culture_group in sorted_culture_groups:
            branches = pivot_data[tenant].get(culture_group, set())
            count = len(branches)
            row_data.append(count if count > 0 else '')
        writer.writerow(row_data)

print("="*120)
print("PIVOT TABLE: TENANT x CULTURE GROUP")
print("="*120)
print(f"\nPivot table created: {output_file}")
print(f"Dimensions: {len(sorted_tenants)} Tenants x {len(sorted_culture_groups)} Culture Groups")
print(f"\nYou can open this file in Excel or Google Sheets to create a visual.")
print("\nSummary statistics:")
print(f"  Total tenants: {len(sorted_tenants)}")
print(f"  Total culture groups: {len(sorted_culture_groups)}")
print(f"  Total data points: {len(rows)}")

# Show sample of the data
print(f"\nSample data (first 10 tenants, first 10 culture groups):")
print("-" * 120)
sample_culture_groups = sorted_culture_groups[:10]
print(f"{'Tenant':<30} | " + " | ".join([cg[:12] for cg in sample_culture_groups]))
print("-" * 120)
for tenant in sorted_tenants[:10]:
    counts = [str(len(pivot_data[tenant].get(cg, set()))) if pivot_data[tenant].get(cg, set()) else '' for cg in sample_culture_groups]
    print(f"{tenant:<30} | " + " | ".join([f"{c:>12}" for c in counts]))

print("="*120)

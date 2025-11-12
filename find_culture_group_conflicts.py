import csv
from collections import defaultdict

# Read the CSV with translation flavor
with open('data_with_translation_flavor.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Debug: Print column names
print(f"Column names: {fieldnames}\n")

# Group branches by their Cultures value
cultures_to_groups = defaultdict(lambda: {'culture_groups': set(), 'branches': []})

for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    culture_group = row.get('Culture Group', '')
    branch = row.get('Branch', '')
    tenant = row.get('Tenant', row.get('tenant', 'N/A'))  # Try both cases
    
    cultures_to_groups[cultures]['culture_groups'].add(culture_group)
    cultures_to_groups[cultures]['branches'].append({
        'branch': branch,
        'culture_group': culture_group,
        'tenant': tenant
    })

# Find conflicts: same cultures but different Culture Groups
conflicts_found = False
conflict_count = 0

print("="*120)
print("BRANCHES WITH SAME CULTURES BUT DIFFERENT CULTURE GROUPS")
print("="*120)

for cultures, data in cultures_to_groups.items():
    if len(data['culture_groups']) > 1:
        conflicts_found = True
        conflict_count += 1
        num_cultures = len(cultures.split(','))
        
        print(f"\n{conflict_count}. Cultures ({num_cultures} languages): {cultures[:80]}{'...' if len(cultures) > 80 else ''}")
        print(f"   Different Culture Groups found: {len(data['culture_groups'])}")
        print(f"   Culture Groups: {', '.join(sorted(data['culture_groups']))}")
        print(f"   Affected branches ({len(data['branches'])}):")
        
        for branch_info in data['branches']:
            print(f"      - {branch_info['branch']} (Tenant: {branch_info['tenant']}, Culture Group: {branch_info['culture_group']})")

if not conflicts_found:
    print("\nNo conflicts found! All branches with the same cultures have the same Culture Group.")
else:
    print(f"\n{'='*120}")
    print(f"SUMMARY: Found {conflict_count} culture groupings with different Culture Groups")
    print(f"{'='*120}")

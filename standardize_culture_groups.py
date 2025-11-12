import csv
from collections import defaultdict

# Read the CSV with translation flavor
with open('data_with_translation_flavor.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Group branches by their Cultures value
cultures_to_groups = defaultdict(lambda: {'culture_groups': set(), 'branches': []})

for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    culture_group = row.get('Culture Group', '')
    
    cultures_to_groups[cultures]['culture_groups'].add(culture_group)
    cultures_to_groups[cultures]['branches'].append(row)

# Find conflicts and fix them
modifications_made = []
conflict_count = 0

print("="*120)
print("STANDARDIZING CULTURE GROUPS - USING SHORTEST NAME FOR EACH CULTURE SET")
print("="*120)

for cultures, data in cultures_to_groups.items():
    if len(data['culture_groups']) > 1:
        conflict_count += 1
        # Find the shortest Culture Group name
        shortest_culture_group = min(data['culture_groups'], key=len)
        num_cultures = len(cultures.split(',')) if cultures else 0
        
        print(f"\n{conflict_count}. Cultures ({num_cultures} languages): {cultures[:80]}{'...' if len(cultures) > 80 else ''}")
        print(f"   Different Culture Groups found: {', '.join(sorted(data['culture_groups']))}")
        print(f"   Shortest Culture Group selected: {shortest_culture_group}")
        print(f"   Standardizing {len(data['branches'])} branches:")
        
        # Update all branches with this culture set to use the shortest Culture Group
        for row in data['branches']:
            old_culture_group = row['Culture Group']
            if old_culture_group != shortest_culture_group:
                print(f"      - Branch: {row['Branch']}")
                print(f"        Changed: {old_culture_group} -> {shortest_culture_group}")
                row['Culture Group'] = shortest_culture_group
                modifications_made.append({
                    'branch': row['Branch'],
                    'old': old_culture_group,
                    'new': shortest_culture_group
                })

# Write updated data to new CSV file
output_file = 'data_standardized_culture_groups.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\n{'='*120}")
print(f"SUMMARY:")
print(f"  Culture sets with conflicts: {conflict_count}")
print(f"  Total modifications made: {len(modifications_made)}")
print(f"  New file created: {output_file}")
print(f"{'='*120}")

if modifications_made:
    print(f"\nDETAILED MODIFICATIONS:")
    for mod in modifications_made:
        print(f"  {mod['branch']}: {mod['old']} -> {mod['new']}")

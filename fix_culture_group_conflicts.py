import csv
from collections import defaultdict

# Read the CSV with assigned culture groups
with open('data_with_assigned_culture_groups.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Group rows by Culture Group (only those starting with GL_)
culture_group_map = defaultdict(list)
for row in rows:
    culture_group = row['Culture Group']
    if culture_group.startswith('GL_'):
        cultures = row['Cultures'].strip('"')
        culture_group_map[culture_group].append({
            'row': row,
            'cultures': cultures
        })

# Check for conflicts and update Culture Group names
updated_count = 0
for culture_group, entries in culture_group_map.items():
    # Get all unique culture groupings for this Culture Group
    unique_cultures = set(entry['cultures'] for entry in entries)
    
    if len(unique_cultures) > 1:
        print(f"\nCONFLICT FOUND in Culture Group: {culture_group}")
        print(f"  Found {len(unique_cultures)} different culture groupings:")
        
        # Need to append number to differentiate
        for entry in entries:
            cultures = entry['cultures']
            num_cultures = len(cultures.split(','))
            
            # Check if already has the number appended
            if not culture_group.endswith(f'_{num_cultures}'):
                # Append the number of cultures
                new_culture_group = f"{culture_group}_{num_cultures}"
                entry['row']['Culture Group'] = new_culture_group
                updated_count += 1
                print(f"    Changed: {culture_group} -> {new_culture_group}")
    else:
        print(f"OK: {culture_group} - All branches have same cultures grouping")

# Write to new CSV file
output_file = 'data_final_culture_groups.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'\n{"="*80}')
print(f'Updated {updated_count} rows with conflicts')
print(f'New file created: {output_file}')
print(f'{"="*80}')

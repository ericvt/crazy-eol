import csv

# Read the CSV with standardized culture groups
with open('data_standardized_culture_groups.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Sort cultures alphabetically
sorted_count = 0
print("="*120)
print("SORTING CULTURES ALPHABETICALLY")
print("="*120)

for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    if cultures:
        # Split by comma, strip whitespace, sort, and rejoin
        culture_list = [c.strip() for c in cultures.split(',')]
        sorted_cultures = ','.join(sorted(culture_list))
        
        if sorted_cultures != cultures:
            print(f"\nBranch: {row['Branch']}")
            print(f"  Before: {cultures}")
            print(f"  After:  {sorted_cultures}")
            row['Cultures'] = sorted_cultures
            sorted_count += 1

# Write updated data to new CSV file
output_file = 'data_sorted_cultures.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\n{'='*120}")
print(f"SUMMARY:")
print(f"  Rows with cultures sorted: {sorted_count}")
print(f"  Rows unchanged: {len(rows) - sorted_count}")
print(f"  New file created: {output_file}")
print(f"{'='*120}")

import csv

# Read the CSV with assigned culture groups
with open('data_with_assigned_culture_groups.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Update TranslationFlavor where Translation Provider Type starts with CtsDownstream
updated_count = 0
for row in rows:
    translation_provider_type = row['Translation Provider Type']
    if translation_provider_type.startswith('CtsDownstream'):
        row['TranslationFlavor'] = 'MT'
        updated_count += 1
        print(f"Branch: {row['Branch']}")
        print(f"  Translation Provider Type: {translation_provider_type}")
        print(f"  TranslationFlavor set to: MT\n")

# Write to new CSV file
output_file = 'data_with_translation_flavor.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'{"="*80}')
print(f'Updated {updated_count} rows with TranslationFlavor = MT')
print(f'New file created: {output_file}')
print(f'{"="*80}')

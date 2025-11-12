import csv

# Read the original CSV
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# Process rows and assign Culture Group where blank
updated_count = 0
for row in rows:
    if row['Culture Group'] == '':
        cultures = row['Cultures'].strip('"')
        if cultures:
            num_cultures = len(cultures.split(','))
            translation_provider_name = row['Translation Provider Name']
            new_culture_group = f'{translation_provider_name}_{num_cultures}'
            row['Culture Group'] = new_culture_group
            updated_count += 1

# Write to new CSV file
output_file = 'data_with_assigned_culture_groups.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Updated {updated_count} rows with blank Culture Group')
print(f'New file created: {output_file}')
print(f'Format used: <Translation_Provider_Name>_<number_of_cultures>')

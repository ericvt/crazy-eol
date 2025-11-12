import csv

# Read the data and update Translation Flavor based on QE/HPE settings
print("Reading data_sorted_cultures.csv...")
rows = []

with open('data_sorted_cultures.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        qe_enabled = row.get('QE/AIPE Enabled', '').strip().upper()
        hpe_enabled = row.get('HPE Enabled', '').strip().upper()
        
        # Apply the new logic
        if qe_enabled == 'TRUE' and hpe_enabled == 'TRUE':
            row['TranslationFlavor'] = 'HPE'
        elif qe_enabled == 'TRUE' and hpe_enabled == 'FALSE':
            row['TranslationFlavor'] = 'AIPE'
        elif qe_enabled == 'FALSE' and hpe_enabled == 'TRUE':
            row['TranslationFlavor'] = 'MTPE'
        elif qe_enabled == 'FALSE' and hpe_enabled == 'FALSE':
            row['TranslationFlavor'] = 'MT'
        else:
            # If values are not TRUE/FALSE, keep original or set to empty
            row['TranslationFlavor'] = row.get('TranslationFlavor', '')
        
        rows.append(row)

print(f"Processed {len(rows)} rows")

# Write the updated data
print("\nWriting updated data to data_sorted_cultures.csv...")
with open('data_sorted_cultures.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n✅ Translation Flavor updated successfully!")

# Show some statistics
flavor_counts = {}
for row in rows:
    flavor = row['TranslationFlavor']
    flavor_counts[flavor] = flavor_counts.get(flavor, 0) + 1

print("\nTranslation Flavor distribution:")
for flavor, count in sorted(flavor_counts.items()):
    print(f"  {flavor}: {count}")

print("\nNext steps:")
print("1. Run: python3 create_pivot_final.py")
print("2. Refresh your browser to see the updated visualization")

import csv

with open('data_sorted_cultures.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    print("Field names:")
    for i, field in enumerate(reader.fieldnames):
        print(f"  {i}: '{field}' (length: {len(field)})")
    
    print("\nFirst row keys and values:")
    first_row = next(reader)
    for key in first_row:
        value = first_row[key]
        print(f"  '{key}' = '{value[:50] if value else 'EMPTY'}'")

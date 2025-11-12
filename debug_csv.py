import csv

with open('data_sorted_cultures.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    print("Column names:")
    print(reader.fieldnames)
    print("\nFirst 3 rows:")
    
    for i, row in enumerate(reader):
        if i < 3:
            print(f"\nRow {i+1}:")
            print(f"  Tenant: '{row.get('Tenant', 'MISSING')}' (len={len(row.get('Tenant', ''))})")
            print(f"  Culture Group: '{row.get('Culture Group', 'MISSING')}' (len={len(row.get('Culture Group', ''))})")
            print(f"  Branch: '{row.get('Branch', 'MISSING')}' (len={len(row.get('Branch', ''))})")
            
            # Check after strip
            tenant = row.get('Tenant', '').strip()
            culture_group = row.get('Culture Group', '').strip()
            branch = row.get('Branch', '').strip()
            print(f"  After strip - Tenant: '{tenant}', CG: '{culture_group}', Branch: '{branch}'")
            print(f"  Conditions: tenant={bool(tenant)}, cg={bool(culture_group)}, branch={bool(branch)}")
        else:
            break

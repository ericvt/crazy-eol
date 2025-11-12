import csv
from collections import defaultdict

# Read data_sorted_cultures.csv and count unique branches per tenant/culture group
branch_counts = defaultdict(lambda: defaultdict(set))
branch_metadata = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # Store metadata per tenant/culture_group/branch
culture_group_cultures = {}  # Store cultures for each culture group
all_culture_groups = set()
all_tenants = set()

print("Reading data_sorted_cultures.csv...")
with open('data_sorted_cultures.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    row_count = 0
    
    for row in reader:
        row_count += 1
        tenant = row.get('Tenant', '').strip()
        culture_group = row.get('Culture Group', '').strip()
        branch = row.get('Branch', '').strip()
        cultures = row.get('Cultures', '').strip()
        translation_flavor = row.get('TranslationFlavor', '').strip()
        qe_enabled = row.get('QE/AIPE Enabled', '').strip()
        hpe_enabled = row.get('HPE Enabled', '').strip()
        
        # Debug first few rows
        if row_count <= 3:
            print(f"Row {row_count}: tenant='{tenant}', culture_group='{culture_group}', branch='{branch}'")
            print(f"  Checks: tenant={bool(tenant)}, cg={bool(culture_group)}, branch={bool(branch)}")
        
        if tenant and culture_group and branch:
            branch_counts[tenant][culture_group].add(branch)
            all_culture_groups.add(culture_group)
            all_tenants.add(tenant)
            
            # Debug BIC_Learn_2_art
            if tenant == 'BIC_Learn_2_art' and culture_group in ['BIC_base_8', 'BIC_Learn_17', 'BIC_Learn8_art_8']:
                print(f"  Storing: {tenant}|{culture_group}|{branch} -> flavor='{translation_flavor}'")
            
            # Store metadata for this combination
            branch_metadata[tenant][culture_group][branch] = {
                'flavor': translation_flavor,
                'qe': qe_enabled,
                'hpe': hpe_enabled
            }
            
            # Store the cultures for this culture group (if not already stored)
            if culture_group not in culture_group_cultures and cultures:
                culture_group_cultures[culture_group] = cultures

print(f"Processed {row_count} rows")
print(f"Found {len(all_tenants)} unique tenants")
print(f"Found {len(all_culture_groups)} unique culture groups")

# Sort tenants alphabetically
sorted_tenants = sorted(all_tenants)

# Sort culture groups by actual number of cultures (least to highest)
def get_culture_count(culture_group):
    """Get the actual count of cultures for a culture group"""
    cultures = culture_group_cultures.get(culture_group, '')
    return len(cultures.split(',')) if cultures else 0

sorted_culture_groups = sorted(all_culture_groups, key=get_culture_count)

# Write pivot table to CSV with metadata
print("\nCreating tenant_culture_group_pivot.csv...")
with open('tenant_culture_group_pivot.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Header row: Culture Group, Number of Cultures, Cultures, then all tenant names
    header = ['Culture Group', 'Number of Cultures', 'Cultures'] + sorted_tenants
    writer.writerow(header)
    
    # Data rows - one row per culture group
    for culture_group in sorted_culture_groups:
        cultures = culture_group_cultures.get(culture_group, '')
        count = len(cultures.split(',')) if cultures else 0
        
        row = [culture_group, count, cultures]
        
        # Add branch counts and metadata for each tenant
        for tenant in sorted_tenants:
            branches = branch_counts[tenant][culture_group]
            branch_count = len(branches)
            
            if branch_count > 0:
                # Determine the predominant flavor/settings
                flavors = []
                qe_true_hpe_false = 0
                qe_true_hpe_true = 0
                
                for branch in branches:
                    meta = branch_metadata[tenant][culture_group][branch]
                    flavors.append(meta['flavor'])
                    if meta['qe'].upper() == 'TRUE':
                        if meta['hpe'].upper() == 'TRUE':
                            qe_true_hpe_true += 1
                        else:
                            qe_true_hpe_false += 1
                
                # Debug BIC_Learn_2_art
                if tenant == 'BIC_Learn_2_art' and culture_group in ['BIC_base_8', 'BIC_Learn_17', 'BIC_Learn8_art_8']:
                    print(f"  Processing cell: {tenant}|{culture_group}")
                    print(f"    Branches: {branches}")
                    print(f"    Flavors collected: {flavors}")
                
                # Determine predominant flavor
                flavor_counts = {}
                for f in flavors:
                    if f:
                        flavor_counts[f] = flavor_counts.get(f, 0) + 1
                
                predominant_flavor = max(flavor_counts.items(), key=lambda x: x[1])[0] if flavor_counts else ''
                
                # Debug BIC_Learn_2_art
                if tenant == 'BIC_Learn_2_art' and culture_group in ['BIC_base_8', 'BIC_Learn_17', 'BIC_Learn8_art_8']:
                    print(f"    Flavor counts: {flavor_counts}")
                    print(f"    Predominant: '{predominant_flavor}'")
                
                # Format: count|flavor|qe_hpe_false|qe_hpe_true
                cell_value = f"{branch_count}|{predominant_flavor}|{qe_true_hpe_false}|{qe_true_hpe_true}"
                row.append(cell_value)
            else:
                row.append('')
        
        writer.writerow(row)

print(f"\nPivot table created successfully!")
print(f"Dimensions: {len(sorted_tenants)} tenants x {len(sorted_culture_groups)} culture groups")
print(f"\nFirst 5 tenants: {sorted_tenants[:5]}")
print(f"First 5 culture groups: {sorted_culture_groups[:5]}")
print(f"\n✅ Files created:")
print(f"   📄 tenant_culture_group_pivot.csv - CSV data file")
print(f"   🌐 pivot_viewer.html - Interactive web viewer")
print(f"\nTo view the interactive visualization, open pivot_viewer.html in your web browser.")

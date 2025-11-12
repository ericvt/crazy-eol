import csv
from collections import defaultdict

# Read the CSV with sorted cultures
with open('data_sorted_cultures.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Count unique culture groupings and their usage
culture_to_branches = defaultdict(list)

for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    if cultures:
        branch = row.get('Branch', 'N/A')
        culture_to_branches[cultures].append(branch)

print("="*120)
print("ALL UNIQUE CULTURE GROUPINGS")
print("="*120)

# Sort by number of cultures, then by frequency
sorted_groupings = sorted(culture_to_branches.items(), 
                         key=lambda x: (len(x[0].split(',')), -len(x[1])))

print(f"\nTotal unique culture groupings: {len(culture_to_branches)}\n")

for i, (cultures, branches) in enumerate(sorted_groupings, 1):
    num_cultures = len(cultures.split(','))
    num_branches = len(branches)
    
    print(f"{i}. Culture Grouping ({num_cultures} language{'s' if num_cultures > 1 else ''})")
    print(f"   Used by: {num_branches} branch{'es' if num_branches != 1 else ''}")
    print(f"   Languages: {cultures}")
    
    # Show first few branches if there are many
    if num_branches <= 5:
        print(f"   Branches: {', '.join(branches)}")
    else:
        print(f"   Branches (showing first 5): {', '.join(branches[:5])}...")
    print()

print("="*120)
print(f"SUMMARY: {len(culture_to_branches)} unique culture groupings found")
print("="*120)

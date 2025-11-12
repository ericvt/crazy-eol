import csv
from collections import defaultdict

# Read the CSV with sorted cultures
with open('data_sorted_cultures.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Count distinct Culture Groups
culture_groups = set()
culture_group_to_branches = defaultdict(list)

for row in rows:
    culture_group = row.get('Culture Group', '').strip()
    branch = row.get('Branch', 'N/A')
    
    if culture_group:
        culture_groups.add(culture_group)
        culture_group_to_branches[culture_group].append(branch)

print("="*120)
print("DISTINCT CULTURE GROUPS ANALYSIS")
print("="*120)

print(f"\nTotal distinct Culture Groups: {len(culture_groups)}")
print(f"Total rows in file: {len(rows)}")

# Show distribution
print(f"\nTop 20 most used Culture Groups:")
print("-" * 80)
sorted_by_frequency = sorted(culture_group_to_branches.items(), 
                            key=lambda x: len(x[1]), reverse=True)

for i, (culture_group, branches) in enumerate(sorted_by_frequency[:20], 1):
    num_branches = len(branches)
    print(f"{i:2d}. {culture_group:50s} - Used by {num_branches:4d} branch{'es' if num_branches != 1 else ''}")

print(f"\nCulture Groups used by only 1 branch: {sum(1 for cg, branches in culture_group_to_branches.items() if len(branches) == 1)}")
print(f"Culture Groups used by 2-5 branches: {sum(1 for cg, branches in culture_group_to_branches.items() if 2 <= len(branches) <= 5)}")
print(f"Culture Groups used by 6+ branches: {sum(1 for cg, branches in culture_group_to_branches.items() if len(branches) >= 6)}")

print(f"\n{'='*120}")

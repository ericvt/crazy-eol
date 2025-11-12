import csv
from collections import defaultdict

# Read the CSV with sorted cultures
with open('data_sorted_cultures.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Count unique culture groupings
unique_cultures = set()
culture_grouping_stats = defaultdict(int)

for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    if cultures:
        unique_cultures.add(cultures)
        # Count how many cultures in this grouping
        num_cultures = len(cultures.split(','))
        culture_grouping_stats[num_cultures] += 1

print("="*120)
print("UNIQUE CULTURE GROUPINGS ANALYSIS")
print("="*120)

print(f"\nTotal unique culture groupings: {len(unique_cultures)}")
print(f"Total rows in file: {len(rows)}")

print(f"\nBreakdown by number of cultures:")
print("-" * 60)
for num_cultures in sorted(culture_grouping_stats.keys()):
    count = culture_grouping_stats[num_cultures]
    print(f"  {num_cultures:2d} culture(s): {count:4d} row(s)")

# Show distribution
culture_to_count = defaultdict(int)
for row in rows:
    cultures = row.get('Cultures', '').strip('"')
    if cultures:
        culture_to_count[cultures] += 1

print(f"\nMost common culture groupings:")
print("-" * 60)
sorted_by_frequency = sorted(culture_to_count.items(), key=lambda x: x[1], reverse=True)
for i, (cultures, count) in enumerate(sorted_by_frequency[:10], 1):
    num_cultures = len(cultures.split(','))
    cultures_display = cultures[:80] + '...' if len(cultures) > 80 else cultures
    print(f"{i:2d}. Used by {count:3d} row(s) - {num_cultures:2d} culture(s): {cultures_display}")

print(f"\n{'='*120}")

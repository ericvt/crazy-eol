import pandas as pd
from collections import Counter

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("CULTURE vs CULTURE GROUPING ANALYSIS")
print("="*80)
print()

# Unique cultures (individual locales like ja-JP, fr-FR)
all_cultures = []
for cultures_str in df['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        all_cultures.extend(cultures_list)

unique_cultures = sorted(set(all_cultures))
print(f"Number of unique CULTURES (individual locales): {len(unique_cultures)}")
print(f"Examples: {', '.join(unique_cultures[:10])}")
print()

# Unique culture groupings
unique_culture_groups = sorted([str(c) for c in df['Culture Group'].unique() if pd.notna(c)])
print(f"Number of unique CULTURE GROUPINGS (named groups): {len(unique_culture_groups)}")
print(f"Examples: {', '.join(unique_culture_groups[:10])}")
print()

# Show the relationship - which cultures belong to which culture groupings
print("CULTURE GROUPING DETAILS (showing first 10 groups):")
print("="*80)
print()

for cg in unique_culture_groups[:10]:
    # Get all rows with this culture group
    rows_with_cg = df[df['Culture Group'] == cg]

    # Extract all cultures from these rows
    cultures_in_group = []
    for cultures_str in rows_with_cg['Cultures'].dropna():
        if isinstance(cultures_str, str):
            cultures_list = [c.strip() for c in cultures_str.split(',')]
            cultures_in_group.extend(cultures_list)

    # Get unique cultures and count
    unique_cultures_in_group = sorted(set(cultures_in_group))

    print(f"Culture Group: {cg}")
    print(f"  Number of unique cultures: {len(unique_cultures_in_group)}")
    print(f"  Cultures: {', '.join(unique_cultures_in_group)}")
    print(f"  Used by {len(rows_with_cg)} rows in dataset")
    print()

# Summary statistics
print("="*80)
print("SUMMARY:")
print("-"*80)
print(f"Total unique individual cultures (locales): {len(unique_cultures)}")
print(f"Total unique culture groupings (named collections): {len(unique_culture_groups)}")
print()

# Show how many cultures each grouping typically contains
print("Distribution of cultures per grouping:")
print("-"*80)
cultures_per_group = []
for cg in unique_culture_groups:
    rows_with_cg = df[df['Culture Group'] == cg]
    cultures_in_group = []
    for cultures_str in rows_with_cg['Cultures'].dropna():
        if isinstance(cultures_str, str):
            cultures_list = [c.strip() for c in cultures_str.split(',')]
            cultures_in_group.extend(cultures_list)
    unique_cultures_in_group = set(cultures_in_group)
    cultures_per_group.append(len(unique_cultures_in_group))

from statistics import mean, median
print(f"  Minimum cultures in a grouping: {min(cultures_per_group)}")
print(f"  Maximum cultures in a grouping: {max(cultures_per_group)}")
print(f"  Average cultures per grouping: {mean(cultures_per_group):.1f}")
print(f"  Median cultures per grouping: {median(cultures_per_group):.0f}")
print()
print("="*80)

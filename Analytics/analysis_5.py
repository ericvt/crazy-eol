import pandas as pd
from collections import Counter

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("ANALYSIS #5")
print("="*80)
print()

# Get all unique cultures
all_cultures = []
for cultures_str in df['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        all_cultures.extend(cultures_list)

# Find the most common culture
culture_counts = Counter(all_cultures)
most_common_culture, most_common_count = culture_counts.most_common(1)[0]

print(f"Most common culture: {most_common_culture}")
print(f"Occurrences: {most_common_count}")
print()

# Get total branches
total_branches = df['Branch'].nunique()

# a) Calculate number of unique branches it is included in
branches_with_culture = df[df['Cultures'].str.contains(most_common_culture, na=False)]['Branch'].nunique()
branches_with_culture_pct = (branches_with_culture / total_branches * 100)

print(f"a) Unique branches including {most_common_culture}:")
print(f"   Count: {branches_with_culture}")
print(f"   Percentage: {branches_with_culture_pct:.2f}% of {total_branches} total branches")
print()

# b) How many unique branches do NOT include that culture
branches_without_culture = total_branches - branches_with_culture
branches_without_culture_pct = (branches_without_culture / total_branches * 100)

print(f"b) Unique branches NOT including {most_common_culture}:")
print(f"   Count: {branches_without_culture}")
print(f"   Percentage: {branches_without_culture_pct:.2f}% of {total_branches} total branches")
print()

print("="*80)

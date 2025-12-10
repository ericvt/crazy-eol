import pandas as pd
import numpy as np
from statistics import mean

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("ANALYSIS #1")
print("="*80)
print()

# A) Unique counts - table only
print("A) UNIQUE COUNTS")
print("="*80)

# Calculate unique counts
unique_tenants = [str(t) for t in df['Tenant'].unique() if pd.notna(t)]
unique_branches = [str(b) for b in df['Branch'].unique() if pd.notna(b)]
unique_categories = [str(c) for c in df['Content Group Category'].unique() if pd.notna(c)]

# Parse cultures from the Cultures field
all_cultures = []
for cultures_str in df['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        all_cultures.extend(cultures_list)
unique_cultures = sorted(set(all_cultures))

unique_flavors = [str(f) for f in df['TranslationFlavor'].unique() if pd.notna(f)]

# Create summary table
summary_data = {
    'Dimension': [
        'Unique Tenants',
        'Unique Branches',
        'Unique Content Group Categories',
        'Unique Cultures',
        'Unique Translation Flavors'
    ],
    'Count': [
        len(unique_tenants),
        len(unique_branches),
        len(unique_categories),
        len(unique_cultures),
        len(unique_flavors)
    ]
}
summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))
print()
print()

# B) Combinations
print("B) COMBINATIONS")
print("="*80)

# Branch to Content Group Category combinations
branch_category_combos = df.groupby(['Branch', 'Content Group Category']).size().reset_index(name='Count')
num_branch_category = len(branch_category_combos)

# Culture groupings count
unique_culture_groups = [str(c) for c in df['Culture Group'].unique() if pd.notna(c)]
num_culture_groups = len(unique_culture_groups)

combinations_data = {
    'Metric': [
        'Branch to Content Group Category Combinations',
        'Culture Groupings'
    ],
    'Count': [
        num_branch_category,
        num_culture_groups
    ]
}
combinations_df = pd.DataFrame(combinations_data)
print(combinations_df.to_string(index=False))
print()
print()

# C) Culture grouping statistics
print("C) CULTURE GROUPING STATISTICS")
print("="*80)

# Calculate cultures per grouping
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

stats_data = {
    'Metric': [
        'Minimum cultures in a grouping',
        'Maximum cultures in a grouping',
        'Average cultures per grouping'
    ],
    'Value': [
        min(cultures_per_group),
        max(cultures_per_group),
        f"{mean(cultures_per_group):.1f}"
    ]
}
stats_df = pd.DataFrame(stats_data)
print(stats_df.to_string(index=False))
print()

print("="*80)

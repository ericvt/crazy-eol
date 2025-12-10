import pandas as pd

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("ANALYSIS #4")
print("="*80)
print()

print("QUESTION: Is there any branch where translation flavor = MT that does")
print("not match the full culture list from 'MT supported locales'?")
print("(Are we missing MT supported cultures for those branches?)")
print("="*80)
print()

# Get MT supported locales from Analysis #3
mt_rows = df[df['TranslationFlavor'] == 'MT']
mt_cultures = []
for cultures_str in mt_rows['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        mt_cultures.extend(cultures_list)

mt_supported_locales = set(mt_cultures)

print(f"MT supported locales count: {len(mt_supported_locales)}")
print()

# Get all branches that have MT flavor
mt_branches = df[df['TranslationFlavor'] == 'MT']['Branch'].unique()

# For each branch with MT, get all cultures used across all MT rows
branch_mt_cultures = {}
for branch in mt_branches:
    branch_mt_data = df[(df['Branch'] == branch) & (df['TranslationFlavor'] == 'MT')]
    cultures_set = set()
    for cultures_str in branch_mt_data['Cultures'].dropna():
        if isinstance(cultures_str, str):
            cultures_list = [c.strip() for c in str(cultures_str).split(',')]
            cultures_set.update(cultures_list)
    branch_mt_cultures[branch] = cultures_set

# Find branches missing MT supported cultures
branches_with_missing = []

for branch, branch_cultures in branch_mt_cultures.items():
    missing_cultures = mt_supported_locales - branch_cultures
    if missing_cultures:
        branches_with_missing.append({
            'Branch': branch,
            'Missing Cultures Count': len(missing_cultures),
            'Has Cultures Count': len(branch_cultures),
            'Coverage %': f"{len(branch_cultures)/len(mt_supported_locales)*100:.1f}%"
        })

if branches_with_missing:
    print(f"RESULT: YES - Found {len(branches_with_missing)} branches with MT flavor")
    print("that are missing some MT supported cultures:")
    print()

    missing_df = pd.DataFrame(branches_with_missing)
    missing_df = missing_df.sort_values('Missing Cultures Count', ascending=False)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(missing_df.to_string(index=False))
    print()
    print(f"Total branches with MT: {len(mt_branches)}")
    print(f"Branches missing some MT cultures: {len(branches_with_missing)} ({len(branches_with_missing)/len(mt_branches)*100:.1f}%)")
    print()
else:
    print("RESULT: NO")
    print()
    print("All branches with MT translation flavor have the complete set of")
    print("MT supported locales.")
    print()

print("="*80)

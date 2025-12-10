import pandas as pd

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("ANALYSIS #3")
print("="*80)
print()

# Get all unique cultures in the dataset
all_cultures = []
for cultures_str in df['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        all_cultures.extend(cultures_list)
all_unique_cultures = sorted(set(all_cultures))

# A) MT Translation Flavor
print("A) MT TRANSLATION FLAVOR")
print("="*80)

# MT supported locales
mt_rows = df[df['TranslationFlavor'] == 'MT']
mt_cultures = []
for cultures_str in mt_rows['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        mt_cultures.extend(cultures_list)

mt_supported = sorted(set(mt_cultures))
print(f"MT supported locales: {len(mt_supported)}")
print(", ".join(mt_supported))
print()

# MT non-supported locales
mt_non_supported = sorted(set(all_unique_cultures) - set(mt_supported))
print(f"MT non-supported locales: {len(mt_non_supported)}")
print(", ".join(mt_non_supported))
print()
print()

# B) AIPE Translation Flavor
print("B) AIPE TRANSLATION FLAVOR")
print("="*80)

# AIPE supported locales
aipe_rows = df[df['TranslationFlavor'] == 'AIPE']
aipe_cultures = []
for cultures_str in aipe_rows['Cultures'].dropna():
    if isinstance(cultures_str, str):
        cultures_list = [c.strip() for c in cultures_str.split(',')]
        aipe_cultures.extend(cultures_list)

aipe_supported = sorted(set(aipe_cultures))
print(f"AIPE supported locales: {len(aipe_supported)}")
print(", ".join(aipe_supported))
print()

# AIPE non-supported locales
aipe_non_supported = sorted(set(all_unique_cultures) - set(aipe_supported))
print(f"AIPE non-supported locales: {len(aipe_non_supported)}")
print(", ".join(aipe_non_supported))
print()

print("="*80)

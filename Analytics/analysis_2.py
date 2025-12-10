import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('../data_processed.csv')

print("="*80)
print("ANALYSIS #2")
print("="*80)
print()

print("A) RELATIONSHIP BETWEEN CONTENT GROUP CATEGORIES AND TRANSLATION FLAVORS")
print("="*80)
print()

# Create a crosstab showing the relationship
relationship = pd.crosstab(
    df['Content Group Category'],
    df['TranslationFlavor'],
    margins=True,
    margins_name='Total'
)

print(relationship)
print()

print("="*80)

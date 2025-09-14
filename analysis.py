# ==========================================================
# CORD-19 ANALYSIS SCRIPT (analysis.py) - FINAL CLEAN VERSION
# This script uses our manually created 'metadata_sample.csv'
# ==========================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

print("--- Starting CORD-19 Data Analysis ---")
print("\nStep 1: Loading our new, small 'metadata_sample.csv' file...")

try:
    df = pd.read_csv('metadata_sample.csv', low_memory=False)
    print(">>> Success! Sample file loaded.")
except FileNotFoundError:
    print(">>> ERROR: 'metadata_sample.csv' not found! Please run the 'create_sample.py' script first.")
    exit()

print("\nStep 2: Cleaning the data...")

# This line fixes the date error by being flexible.
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Drop any rows that are unusable (missing dates, titles, etc.)
df.dropna(subset=['publish_time', 'title', 'journal'], inplace=True)

# Extract the year from the date.
df['year'] = df['publish_time'].dt.year
df['year'] = df['year'].astype(int)

df_cleaned = df[df['year'] >= 2019]

print(">>> Success! Data is cleaned and prepared.")
print("\nStep 3: Saving the final clean file for our app...")

cleaned_filename = 'cleaned_cord_metadata.csv'
df_cleaned.to_csv(cleaned_filename, index=False)

print(f"\n>>> Success! The final file has been saved as '{cleaned_filename}'")
print("\n--- Analysis Script Finished ---")
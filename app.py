# ==========================================================
# CORD-19 STREAMLIT APP (app.py) - FINAL CLEAN VERSION
# This script reads our 'cleaned_cord_metadata.csv' to build the web app.
# ==========================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# --- 1. Page Configuration and Title ---
# We start by setting a title for our web app, which appears in the browser tab.
# Then we create a main title and a short description on the page itself.
st.set_page_config(page_title="CORD-19 Data Explorer")
st.title("CORD-19 Research Paper Explorer")
st.write("An interactive web app to explore trends in COVID-19 research papers.")


# --- 2. Data Loading ---
# This function loads our small, clean data file.
# The line "@st.cache_data" is a magic Streamlit command. It's like telling
# the app: "Load this data once, and keep it in your memory. Don't waste time
# reloading it every time the user moves a slider." This makes the app VERY fast.
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_cord_metadata.csv')
    return df

# We call the function to load the data into a dataframe called 'df'.
df = load_data()


# --- 3. First Visualization: Publications Over Time ---
st.header("1. How much research was published over time?")
st.write("This chart shows the total number of research papers published each year.")

# Create the data for the plot
papers_by_year = df['year'].value_counts().sort_index()

# Create a figure and axis for our plot using matplotlib.
# This is the proper way to create plots that will be shown in Streamlit.
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(papers_by_year.index.astype(str), papers_by_year.values, color='teal') # astype(str) treats years as categories
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.set_title("CORD-19 Publications by Year")

# Display our first plot in the Streamlit app.
st.pyplot(fig1)


# --- 4. Second Visualization (Interactive): Top Journals by Year ---
st.header("2. Which journals published the most papers?")
st.write("Use the slider below to select a specific year and see the top 10 publishing journals.")

# Here is our interactive widget!
# We define a slider that goes from the minimum year in our data to the maximum, starting at 2020.
min_year = df['year'].min()
max_year = df['year'].max()
selected_year = st.slider("Select a Year", min_value=min_year, max_value=max_year, value=2020)

# We filter our data based on whatever year the user has currently selected on the slider.
filtered_data_by_year = df[df['year'] == selected_year]

# Find the top 10 journals for that filtered data.
top_journals_by_year = filtered_data_by_year['journal'].value_counts().head(10)

# Create our second plot.
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_journals_by_year.values, y=top_journals_by_year.index, palette='viridis', ax=ax2)
ax2.set_xlabel("Number of Papers Published")
ax2.set_ylabel("Journal Name")
ax2.set_title(f"Top 10 Journals in {selected_year}")

# Display our interactive plot.
st.pyplot(fig2)


# --- 5. Third Visualization: Word Cloud of Titles ---
st.header("3. What were the most common words in paper titles?")
st.write(f"This word cloud shows the most frequent words in paper titles for the year {selected_year}.")

# We create a single, giant string of text containing all the paper titles from the selected year.
# We also make sure every word is lowercase to count "Covid" and "covid" as the same word.
text_for_wordcloud = " ".join(title.lower() for title in filtered_data_by_year.title)

# Create the word cloud object and generate the cloud from our text.
wordcloud = WordCloud(stopwords=None, background_color="white", colormap='plasma', max_words=100).generate(text_for_wordcloud)

# Create our third plot.
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off") # Hide the ugly x and y axis lines for a cleaner look.
st.pyplot(fig3)
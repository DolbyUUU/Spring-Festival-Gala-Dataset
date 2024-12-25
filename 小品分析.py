import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
file_path = '春晚小品40年_分析_BERT.xlsx'
df = pd.read_excel(file_path)

# Calculate the number of actors for each sketch
df['Number of Actors'] = df['表演者'].str.split('、').apply(len)

# Calculate the average number of actors per sketch for each year
average_actors_per_year = df.groupby('年份')['Number of Actors'].mean()

# Plot the line chart for average number of actors
plt.figure(figsize=(12, 6))
average_actors_per_year.plot(kind='line', marker='o')
plt.title('\n\nAverage Number of Actors per Sketch by Year')
plt.xlabel('Year')
plt.ylabel('Average Number of Actors')
plt.grid(True)
plt.tight_layout()
plt.savefig('average_actors_per_year.png')

# Calculate the average number of sketches per year
average_sketches_per_year = df.groupby('年份')['节目名'].nunique()

# Plot the line chart for average number of sketches
plt.figure(figsize=(12, 6))
average_sketches_per_year.plot(kind='line', marker='o')
plt.title('\n\nAverage Number of Sketches by Year')
plt.xlabel('Year')
plt.ylabel('Average Number of Sketches')
plt.grid(True)
plt.tight_layout()
plt.savefig('average_sketches_per_year.png')

# Calculate the word count of dialogues for each sketch
df['Word Count'] = df['台词'].apply(lambda x: len(str(x).split()))

# Calculate the average word count of dialogues per sketch per year
average_word_count_per_year = df.groupby('年份')['Word Count'].mean()

# Plot the line chart for average word count of dialogues
plt.figure(figsize=(12, 6))
average_word_count_per_year.plot(kind='line', marker='o')
plt.title('\n\nAverage Word Count of Dialogues per Sketch by Year')
plt.xlabel('Year')
plt.ylabel('Average Word Count')
plt.grid(True)
plt.tight_layout()
plt.savefig('average_word_count_per_sketch_per_year.png')

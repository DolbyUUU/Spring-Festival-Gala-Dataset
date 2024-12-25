import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取数据
file_path = '春晚小品40年_分析_BERT.xlsx'
df = pd.read_excel(file_path)

# 将表演者列分割成多行
s = df['表演者'].str.split('、').apply(pd.Series, 1).stack()
s.index = s.index.droplevel(-1)
s.name = '演员'
del df['表演者']
df = df.join(s)

# 出演小品次数最多的TopN演员和对应的次数
def top_actors_by_appearances(df, top_n):
    return df['演员'].value_counts().head(top_n)

# 设置TopN的值
top_n = 30

# 执行分析并保存结果到txt文件
results = "出演小品次数最多的前{}演员和对应的次数:\n".format(top_n)
results += top_actors_by_appearances(df, top_n).to_string()
results += '\n\n'

# 设置筛选的最小出演次数
min_times = 7

# 设置TopN的值
top_n = 5

# 定义分数列
score_columns = ['讽刺性（1-10）', '内容概括情感', '台词情感']

# 计算每位演员的演出次数
actors_counts = df['演员'].value_counts()

# 过滤出演出次数超过min_times的演员
eligible_actors = actors_counts[actors_counts > min_times].index

# 过滤DataFrame以包含演出次数超过min_times的演员
df_eligible = df[df['演员'].isin(eligible_actors)]

# 对每个分数类别计算平均分数最高和最低的TopN演员
for score in score_columns:
    grouped_actors = df_eligible.groupby('演员')[score].mean()
    top_actors_highest = grouped_actors.sort_values(ascending=False).head(top_n)
    top_actors_lowest = grouped_actors.sort_values(ascending=True).head(top_n)
    
    results += f"{score}平均分数最高的前{top_n}演员:\n"
    results += top_actors_highest.to_string()
    results += f"\n{score}平均分数最低的前{top_n}演员:\n"
    results += top_actors_lowest.to_string()
    results += '\n\n'

# Define the file path
file_path = 'top_actors_results.txt'

# Check if the file exists and delete it
if os.path.exists(file_path):
    os.remove(file_path)

# Now, open the file in write mode (which will create a new file) and write the results
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(results)

# 生成词云的字典，键是演员名称，值是出现频次
eligible_actors_freq = {actor: actors_counts[actor] for actor in eligible_actors}

# 生成词云
wordcloud = WordCloud(
    font_path='msyh.ttc',  # 设置字体路径，确保支持中文（这里是微软雅黑字体）
    width=800,
    height=400,
    background_color='white'
).generate_from_frequencies(eligible_actors_freq)  # 使用频次字典生成词云

# 展示词云
plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 关闭坐标轴
plt.title('\n\nWord Cloud of Actor Participation Frequency')

# 保存词云到文件
plt.savefig('actor_participation_wordcloud.png', format='png', bbox_inches='tight')
import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
file_path = '春晚小品40年_分析_BERT.xlsx'
data = pd.read_excel(file_path)

# 创建一个分数列表，包含所有要分析的列
score_columns = ['讽刺性（1-10）', '内容概括情感', '台词情感']

# 定义相应的英文翻译
english_columns = ['Satirical (1-10)', 'Summary Sentiment', 'Dialogue Sentiment']

# 创建一个颜色列表，以便每个图表使用不同的颜色
colors = ['blue', 'red', 'green']

# 创建一个字典来存储每个分数的年平均值
average_scores_by_year = {}

# 循环计算每个分数的年平均值
for column in score_columns:
    average_scores_by_year[column] = data.groupby('年份')[column].mean()

# 绘制每个分数的曲线图
for index, (column, english_column, color) in enumerate(zip(score_columns, english_columns, colors)):
    plt.figure(figsize=(14, 7))
    plt.plot(average_scores_by_year[column], marker='o', color=color)
    
    # 自定义x轴
    start, end = data['年份'].min(), data['年份'].max()
    plt.xticks(range(start, end + 1, 2), rotation=45)
    
    # 设置标题和标签
    plt.title(f'\n\nAverage {english_column} by Year (1983-2023)')
    plt.xlabel('Year')
    plt.ylabel(f'Average {english_column}')
    
    # 进一步调整布局
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{column}.png', dpi=300)
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 读取数据
file_path = '春晚小品40年_分析_BERT.xlsx'
df = pd.read_excel(file_path)

# 计算每个小品的台词中是否含有“饺子”和“包饺子”
df['含有饺子'] = df['台词'].str.contains('饺子')
df['含有包饺子'] = df['台词'].str.contains('包饺子')

# 统计历年春晚的小品中，含有“饺子”和“包饺子”的数量
count_dumplings_per_year = df.groupby('年份')['含有饺子'].sum()
count_making_dumplings_per_year = df.groupby('年份')['含有包饺子'].sum()

# 画出含有“饺子”的折线图
plt.figure(figsize=(12, 6))
ax1 = count_dumplings_per_year.plot(kind='line', marker='o', color='blue')
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))  # 设置y轴为整数
plt.title('\n\nNumber of Sketches Containing "Dumplings" per Year')
plt.xlabel('Year')
plt.ylabel('Number of Sketches with "Dumplings"')
plt.grid(True)
plt.tight_layout()
plt.savefig('sketches_with_dumplings_per_year.png')
plt.close()  # 关闭图表

# 画出含有“包饺子”的折线图
plt.figure(figsize=(12, 6))
ax2 = count_making_dumplings_per_year.plot(kind='line', marker='o', color='green')
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))  # 设置y轴为整数
plt.title('\n\nNumber of Sketches Containing "Making Dumplings" per Year')
plt.xlabel('Year')
plt.ylabel('Number of Sketches with "Making Dumplings"')
plt.grid(True)
plt.tight_layout()
plt.savefig('sketches_with_making_dumplings_per_year.png')
plt.close()  # 关闭图表
import pandas as pd
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

# 读取数据
file_path = '春晚小品40年_分析_BERT.xlsx'
data = pd.read_excel(file_path)

# 加载停用词
stopwords = set()
with open('chinese_stopwords.txt', 'r', encoding='utf-8') as f:
    for line in f:
        stopwords.add(line.strip())

# 可以在这里添加额外的停用词
additional_stopwords = {'小品', '最终', '演员', '之间', '中', 
                        '展现', '讲述', '故事', '对话', '人', 
                        '一个', '一系列', '一对', '一位', '两位', '两人', 
                        '幽默', '笑料', '表演', '互动', '表达', '传达', 
                        '表现', '呈现', '现象', '都', '不', '却', 
                        '误会', '矛盾', '争吵', '讽刺', '混乱',
                        '背景', '情节', '夸张', '方式', '重要性', 
                        '过程', '发生', '引发', '包括', '导致', 
                        '笑话', '误解', '理解'} 
stopwords.update(additional_stopwords)

# 定义年份范围
decades = [(1984, 1993), (1994, 2003), (2004, 2013), (2014, 2023)]

# 中文字段名到英文的映射
column_name_translation = {
    '内容概括': 'Summary'
}

def create_word_cloud(start_year, end_year, column_name, stopwords):
    # 选择当前年份范围内的数据
    mask = (data['年份'] >= start_year) & (data['年份'] <= end_year)
    decade_data = data.loc[mask]
    
    # 合并该年份范围内的文本内容
    text = ''.join(decade_data[column_name].tolist())
    
    # 使用jieba进行中文分词
    text_cut = jieba.cut(text, cut_all=False)
    
    # 剔除停用词
    text_cut_cleaned = ' '.join(word for word in text_cut if word not in stopwords)
    
    # 创建词云对象
    wordcloud = WordCloud(font_path='msyh.ttc',  # 指定中文字体路径
                          width=800, height=400,
                          background_color='white').generate(text_cut_cleaned)
    
    # 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.title(f'\n{start_year}-{end_year} Word Cloud of {column_name_translation[column_name]}')
    
    # 保存词云图片，使用英文字段名
    plt.savefig(f'WordCloud_{column_name_translation[column_name]}_{start_year}_{end_year}.png', dpi=300)
    plt.close()  # 关闭图形，以避免内存中打开太多图形

# 对每个年份范围和每个字段生成词云
for start_year, end_year in decades:
    for column_name in ['内容概括']:
        create_word_cloud(start_year, end_year, column_name, stopwords)
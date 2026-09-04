import pandas as pd
from matplotlib import pyplot as plt
#%%
# 设置中文（防乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#%%
df = pd.read_csv('mcdonalds.csv')
#%%
df.info()
#%%
df.shape
#%%
df.head()
#%%
df.tail()
#%%
df['Like'].unique()
#%%
print('开始清洗数据'+'-'*100)
#%%
print('观察到：有人同时对一件商品表现出觉得既昂贵又便宜\n'
      '但这种情况在现实生活中或许很少见\n'
      '个人认为这是一个无法处理的脏数据')
#%%
print('该列名为汉语')
#%%
df.columns = ['序号',' 美味的','方便的','辣的','易胖的','油腻的','快速的','便宜的','好吃的','昂贵的','健康的',' 恶心的','喜好程度','年龄','光顾频率','性别']

#%%
df.head()
#%%
type(df.columns)
#%%
df.columns
#%%
print('把喜好程度这一列中有文字的内容改成纯数字')
#%%
# df['喜好程度'].replace('I love it!+5',+5,inplace=True)
# df['喜好程度'].replace('I hate it!-5','-5',inplace=True)
#%%
df['喜好程度'] = df['喜好程度'].replace('I love it!+5', '+5')
df['喜好程度'] = df['喜好程度'].replace('I hate it!-5', '-5')
#%%
df['喜好程度'].unique()
#%%
# df['喜好程度'].dtype('number')
#pd.to_numeric() 能自动识别 "+5" 和 "-5"，并转成 5 和 -5
# 如果有无法转换的值，可以设置 errors='coerce' 把它变成 NaN
df['喜好程度'] = pd.to_numeric(df['喜好程度'], errors='coerce')
#%%
df['喜好程度'].unique()
#%%
print('开始对数据进行分析')
#%%
sex_like = df.groupby('性别').agg({'喜好程度':'sum'})
print(sex_like)
#%%
print('给年龄排个组别')
#%%
df.head()
df['年龄'].unique()
#%%
df['年龄等级'] = df['年龄'].apply(lambda x:'老年' if 100>=x>55 else '中年' if 55>=x>35 else '青年' if 35>=x>18 else '少年' if 18>=x>0 else 'none')
#%%
df.head()
#%%
print('按照年龄组别给喜好程度排序')
#%%
yeargroup_like = df.groupby('年龄等级').agg({'喜好程度':'sum'}).sort_values('喜好程度', ascending=False)
print(yeargroup_like)
#%%
print('开始准备画图'+'-'*100)
#%%
fig, axes = plt.subplots(1, 1, figsize=(14, 10))
#%%
axes.bar(yeargroup_like.index,yeargroup_like['喜好程度'],color='green')
#%%
axes.set_title('比较各个年龄段对麦当劳的喜爱程度')
axes.set_xlabel('年龄组别');axes.set_ylabel('喜爱程度')
#%%
axes.tick_params(axis='x', rotation=45)  # X轴标签旋转45度
#%%
plt.savefig('完整麦当劳分析报告.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ 分析完成！图片已生成。")

#%%
print('开始文字报告输出'+'-'*100)
#%%
with open('mcdonalds_report.txt','w',encoding='utf-8') as f:
    f.write(f'关于男女性别对麦当劳的喜爱程度：\n{sex_like.to_string()}\n')
with open ('mcdonalds_report.txt','a',encoding='utf-8') as f:
    f.write(f'关于各个年龄组别对麦当劳的喜爱程度:\n{yeargroup_like.to_string()}\n')
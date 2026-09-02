import pandas as pd
import matplotlib.pyplot as plt
#%%
# ========== 2. 中文设置 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#%%
print('查看原数据大致情况'+'-'*100)
df = pd.read_excel('D:\\my python code\\每日一题的文件夹\\大型商超客户采购数据分析\\SuperStore.xlsx')
#%%
print(df.head())
#%%
df.info()
#%%
df.shape
#%%
print('数据清洗工作'+'-'*100)
#%%
df.head()
#%%
df.isnull().sum()
print('由现在的情况可知，只有邮政编码是未知的，但是又没有办法去一个个查各个地区的邮政编码，以及邮政编码对分析并无太大影响，所以不对此进行处理')
#%%
print('现在开始对的数据进行一些处理'+'-'*100)
#%%
df.columns = ['序列ID','订单ID','运输模式','客户ID','客户名称','客户细分类型','城市','客户所属地区','国家','邮政编码','市场','发货地区','产品ID','产品类别','子类别','产品名称','售价','数量','折扣','利润','运费','订单优先级','订单日期','订单月份','订单月份(num)','订单年份']
print('修改数据的列标签为汉语')
#%%
df.head()
#%%
print('按照利润给该数据进行排一下序，从高到低')
df_profit = df.sort_values(by='利润',ascending=False)
df_profit.head()
#%%
print('下面开始画图的准备工作'+'-'*100)
#%%
print('查看一下折扣都有多少')
discount = df['折扣'].unique()
print(discount)
print('想要查看折扣跟利润的关系:画散点图')
#%%
print('查看一下国家都有哪些')
country = df['国家'].unique()
print(country)
#%%
print('按照国家分组，比较一下每个国家的总利润，用柱状图')
#算是长了一个知识点，在使用agg这个函数的时候如果传入字典，那么生成dataframe对象，如果传入一个函数，那么生成一个series对象
lucrative_10country = df.groupby('国家').agg({'利润':'sum'}).sort_values('利润',ascending=False).head(10)
print(lucrative_10country)
print(type(lucrative_10country))
#这个生成series对象
df['国家'].value_counts()
print('由上面代码输出的内容可知，该数据中的每行数据的所属国家总共有147个\n'
      '故，不适合给全部国家做图表，但是可以只查看前10利润的国家')
#%%
print('按照国家分组，比较一下每个国家的平均折扣，用柱状图')
print('下面查看总折扣前10的国家')
#这个生成dataframe对象
discount_10country = df.groupby('国家').agg({'折扣':'mean'}).sort_values('折扣',ascending=False).head(10)
print(discount_10country)
#%%
print('下面求每年的总利润')
#%%
df['订单年份'].value_counts()
#%%
year_profit = df.groupby('订单年份')['利润'].sum()
print(type(year_profit))
#%%
print('开始画图'+'-'*100)
#%%
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
#%%
axes[0,0].scatter(df['利润'], df['运费'], alpha=0.5)
axes[0,0].set_title('1.利润与运费的关系探究')
axes[0,0].set_xlabel('利润');axes[0,0].set_ylabel('运费')
#%%
axes[0,1].bar(lucrative_10country.index, lucrative_10country['利润'],color='orange')
axes[0,1].set_title('2.总利润在前十的国家利润分布')
axes[0,1].set_xlabel('国家');axes[0,1].set_ylabel('总利润')
axes[0, 1].tick_params(axis='x', rotation=45)  # X轴标签旋转45度
#%%
axes[1,1].bar(discount_10country.index,discount_10country['折扣'],color='red')
axes[1,1].set_title('4.平均折扣在前十的国家折扣分布')
axes[1,1].set_xlabel('国家');axes[1,1].set_ylabel('平均折扣')
axes[1,1].tick_params(axis='x', rotation=45)
#%%
axes[1,0].plot(year_profit.index,year_profit.values,color='green', marker='o')
axes[1,0].set_title('3.年份的总利润趋势')
axes[1,0].set_xlabel('年份');axes[1,0].set_ylabel('总利润')
axes[1,0].tick_params(axis='x', rotation=45)
#%%
# 调整间距，防止重叠
plt.tight_layout()

# ========== 第6块：保存和输出（5行） ==========
plt.savefig('大型商超客户采购分析报告.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ 分析完成！图片已生成。")


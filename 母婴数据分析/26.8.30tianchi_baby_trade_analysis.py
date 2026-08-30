#%%
# 任务一：数据读取与整体了解
#
# 用 read_csv 读取你的CSV文件。
#
# 用 shape 打印行数和列数。
#
# 打印各列缺失值数量，然后处理 property 列的缺失值（直接删除缺失行，因为该列是字符串类型，不适合用平均值填充）。
#
# 任务二：购买行为分析
#
# 用 value_counts 统计 buy_mount 列中，购买数量分别是1、2、3……的商品各有多少条记录，并打印前5个最常见的购买数量。
#
# 分析：绝大多数用户一次购买几件商品？（你只需要描述，不用写代码）
#
# 任务三：时间趋势分析
#
# 把 day 列转换成日期格式（它目前是类似 20140919 的整数）。
#
# 提取年份，统计每年有多少条交易记录。
#
# 画一个柱状图，展示每年交易量的变化趋势。
#
# 任务四：商品类目分析
#
# 用 value_counts 统计 cat1 列中，出现次数最多的前10个商品类目。
#
# 画一个水平条形图，展示这10个类目的交易量。
#
# 任务五：写入报告
# 把统计结果（缺失值处理情况、最常见购买数量、每年交易量、前10类目交易量）写入 analysis_report.txt 文件。
#
# 任务六：添加注释
# 为每个功能块添加清晰注释。
#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
# 设置中文（防乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#%%
print('数据清洗'+'-'*100)
#%%
print('先获取基本文件信息')
df = pd.read_csv('(sample)sam_tianchi_mum_baby_trade_history.csv')
#%%
df.head()
#%%
df.info()
#%%
df.describe()
#%%
df.shape
#%%
df.columns
#%%
df_chinese = df.rename(columns={'user_id':'用户ID','auction_id':'拍卖ID','cat_id':'分类ID','cat1':'一级分类','property':'属性','buy_mount':'购买数量','day':'购买日期'})
#%%
print('已修改表头名为汉语'
      '\n'
      '注：未保存汉语文件')
df_chinese.head()
#%%
df.isnull().sum()
#%%
print('已统计缺失值')
#%%
print('正在删除含有缺失值的列的行')
#把property这一列中含有缺失值的行全部删除了
df.dropna(subset='property',inplace=True)
#%%
print('现已确定property这一列中含有缺失值的行已全部删除')
print('缺失值删除的原因：'
      '1.在总行数在三万行的基础下，那几百行几乎不占有太大的比例'
      '2.在分析数据时，首先要保证的是数据的正确性'
      '3.如果缺失值是字符串而不是数字的话，那就没办法用那些平均值中位数来填充'
      '综上所述，在这个情况下删除是最佳选择')
df.head()
df.info()
#%%
df.isnull().sum()
#%%
#返回每个购买数量对应的记录条数，而且默认按出现次数从高到低排
# print(df['buy_mount'].value_counts())
#现在不仅从高到低排序，并且只显示前5个
print(df['buy_mount'].value_counts().head(5))
print('已用 value_counts 统计 buy_mount 列中，购买数量分别是1、2、3……的商品各有多少条记录，并打印前5个最常见的购买数量。')
#%%
print('由此可知，只买一件商品的购买次数高达26214次，远超购买两件商品的购买次数1790'+'\n'
      '故购买一件商品的购买次数最多')
#%%
#day 列是 20140919 这样的整数，Pandas 默认会把它当成纳秒时间戳来解析，结果全变成 1970-01-01，年份全部变成 1970
# df['day'] =  pd.to_datetime(df['day'])
#加上 format='%Y%m%d'，告诉 Pandas "这是年月日格式的整数"，它才能正确解析
df['day'] = pd.to_datetime(df['day'], format='%Y%m%d')
df.head()
#%%
df['year'] = df['day'].dt.year
print('已把年份提取出来')
df.head()
#%%
df_chinese.head()
#%%
print('已统计每年的购买数量')
year_mount = df.groupby('year')['buy_mount'].sum()
print(year_mount)
#%%
print('正在统计交易量在前10的1级分类')
cat_Trading = df['cat1'].value_counts().head(10)
# 关键修复：将索引转为字符串，避免被当作数值映射
#不知道能不能成功，反正我的心已经慌死了。这已经做了将近3个小时，快4个小时了吧？应该是没有4个小时，但是真的很麻烦
cat_Trading.index = cat_Trading.index.astype(str)
print(cat_Trading)
#%%
print('开始画图'+'-'*100)
fig, axes = plt.subplots(1, 2, figsize=(12, 14))
#%%
#align='center' 是让柱子对齐在 x 轴刻度中间
print('设定好柱形图x轴跟y轴的值和图像颜色等参数')
axes[0].bar(year_mount.index,year_mount.values,align='center',color='orange')
print("设定标题")
axes[0].set_title('每年交易量的变化趋势')
print('设定x轴和y轴的单位')
axes[0].set_xlabel('年份');axes[0].set_ylabel('每年交易量')

#%%
print('每年交易量的变化趋势柱状图已完毕')
#%%
df.head()
#%%
axes[1].barh(cat_Trading.index,cat_Trading.values,align='center',color='black')
axes[1].set_title('商品类目分析')
axes[1].set_xlabel('商品类目');axes[1].set_ylabel('交易量')
plt.show()
print('1级分类的交易量水平条形图已完毕')
#%%
plt.tight_layout()
print('调整间距，防止重叠')
#%%
print('生成图片')
plt.savefig('母婴数据分析报告.png', dpi=300, bbox_inches='tight')
plt.show()
print('可视化工作已完毕'+'-'*100)
#%% md
#把统计结果（缺失值处理情况、最常见购买数量、每年交易量、前10类目交易量）写入 analysis_report.txt 文件。
#%%
print('开始进行文字报告工作'+'-'*100)
with open ('analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write('下面是本次数据分析的统计结果')

#%%
with open('analysis_report.txt', 'a', encoding='utf-8') as f:
    f.write(f'缺失值处理情况:'+'\n'
            f'原本有144个缺失值，现已全部处理')
    f.write('\n')
    f.write(f'最常见购买数量为1次')
    f.write (f'\n')
    f.write(f'这告诉我们，我们的商品大多可能是因为广告或者噱头吸引进来的，所以我们的产品应该加强我们的产品特点，并把品质排在靠前的位置')
    f.write(f'\n')
    # f'每年交易量为：{year_mount.index:year_mount.values}'
            # f'\n'
            # f'前10类目交易量为：{cat_Trading.index:cat_Trading.values}')
            #这两种写法是不对的，正确的应该是下面
    f.write(f'每年交易量为：{year_mount.to_string()}\n')
    f.write(f'前10类目交易量为：{cat_Trading.to_string()}')

#%%
print('文字报告工作已完毕'+'-'*100)


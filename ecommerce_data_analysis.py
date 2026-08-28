# 题目：电商数据分析全流程
# 任务一：数据清洗
# 检查 df 中每一列的缺失值数量，并打印出来。
#
# 用该列的平均值填充 销售额 和 利润 的缺失值。
#
# 任务二：按品类统计
# 按 品类 分组，用 agg 计算每个品类的总销售额和平均利润。
#
# 将结果按总销售额从高到低排序，并打印。
#
# 任务三：按月分析趋势
# 从 订单日期 中提取月份，创建一个新列 月份。
#
# 按 月份 分组，计算每月的总销售额。
#
# 用 matplotlib 画一个折线图，展示1到12月的销售额变化趋势。
#
# x轴：月份
#
# y轴：销售额
#
# 标题：月度销售额趋势
#
# 记得显示网格（grid）
#
# 任务四：客户等级分析
# 按 客户等级 分组，计算每个等级的订单数量和总利润。
#
# 用 matplotlib 画一个柱状图，展示不同客户等级的总利润对比。
#
# x轴：客户等级
#
# y轴：总利润
#
# 标题：客户等级利润对比
#
# 任务五：添加注释
# 为每个功能块添加清晰的注释。


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(42)
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
df = pd.DataFrame({
    '订单日期': np.random.choice(dates, 1000),
    '品类': np.random.choice(['电子产品','服装','食品','日用品'], 1000),
    '销售额': np.round(np.random.uniform(50, 500, 1000), 2),
    '利润': np.round(np.random.uniform(-50, 100, 1000), 2),
    '客户等级': np.random.choice(['普通','银卡','金卡'], 1000, p=[0.6,0.3,0.1])
})
# 故意制造缺失值
df.loc[np.random.choice(df.index, 50), '销售额'] = np.nan
df.loc[np.random.choice(df.index, 30), '利润'] = np.nan

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print(df.head())
print(df.info())
print(df.describe())

#缺失值的数量
print(df.isnull().sum())

#.fillna这个函数内部指定的话，是要以字典的形式
df.fillna({'销售额':df['销售额'].mean(),'利润':df['利润'].mean()}, inplace=True)


#分组也是当如果我们要求的类别有多个，并且多个类别对应有多个不同的计算方法时，也需要用字典的形式
df_kind = df.groupby('品类').agg({'销售额':'sum','利润':'mean'})
print(df_kind)

#ascending上升的
df_res = df_kind.sort_values(by = '销售额', ascending = False)
print(df_res)

#订单日期 列是日期类型，用 .dt.month 就能直接取出1到12的月份数字。
df['月份'] = df['订单日期'].dt.month

df.groupby('月份').agg({'销售额':'sum'})

#返回的是一个DataFrame对象
month_sales = df.groupby('月份').agg({'销售额':'sum'})
print(month_sales)

#figsize这个是尺码
fig, axes = plt.subplots(2,1,figsize=(14, 10))

#现在创建的画布是一维的，只能用axes[0]来表示
#plot 方法需要的是具体的数据值，而不是字符串列名。
# axes[0, 0].plot('月份','月销售额')
axes[0].plot(month_sales.index, month_sales.values)
#这是加上标题
# axes[0,0].set_title('月度销售额趋势')
axes[0].set_title('月度销售额趋势')
axes[0].set_xlabel('月份');axes[0].set_ylabel('月销售额')
#这个是加上网格
axes[0].grid(True)

print(df)

#利用数出订单日期的总数量来间接求出总的订单数量
df.groupby('客户等级').agg({'订单日期':'count', '利润':'sum'})
df.groupby('客户等级')['利润'].agg('sum')

axes[1].bar(df.groupby('客户等级')['利润'].agg('sum').index,df.groupby('客户等级')['利润'].agg('sum').values, color='orange')
axes[1].set_title('客户等级利润对比')
axes[1].set_xlabel('客户等级'); axes[1].set_ylabel('总利润')

# 调整间距，防止重叠
plt.tight_layout()

plt.savefig('完整分析报告.png', dpi=300, bbox_inches='tight')
plt.show()
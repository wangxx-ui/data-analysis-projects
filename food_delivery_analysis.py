# 任务一：数据保存
#
# 把 df 保存为 外卖脏数据.csv。
#
# 任务二：数据清洗
#
# 用 read_csv 读回数据。
#
# 检查各列缺失值数量。
#
# 用每列平均值填充 评分 和 配送时间 的缺失值。
#
# 删除 销量 缺失的行。
#
# 把 配送时间 中大于 120 分钟的值，替换为该列平均值。
#
# 任务三：店铺分析
#
# 按 店铺 分组，用 agg 求每个店铺的总销量和平均评分。
#
# 将结果按总销量从高到低排序，并打印。
#
# 任务四：时间趋势
#
# 从 日期 提取星期几，创建新列 星期。
#
# 按 星期 分组，计算每日总销量。
#
# 画一个折线图，展示一周内销量变化趋势。
#
# 任务五：订单状态分析
#
# 统计每种 订单状态 的数量。
#
# 画一个饼图，展示订单状态占比。
#
# 任务六：添加注释
# 为每个功能块添加清晰注释。

import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range('2024-07-01', '2024-07-31', freq='D')
shops = ['老张炒饭', '湘味小炒', '蜀香麻辣烫', '鲜粥铺', '炸鸡队长']
df = pd.DataFrame({
    '日期': np.random.choice(dates, 800),
    '店铺': np.random.choice(shops, 800),
    '销量': np.random.randint(20, 200, 800).astype(float),
    '评分': np.round(np.random.uniform(3.5, 5.0, 800), 1),
    '配送时间': np.random.randint(15, 60, 800).astype(float),
    '订单状态': np.random.choice(['已完成','已取消','配送中'], 800, p=[0.7, 0.2, 0.1])
})
# 制造缺失值
df.loc[np.random.choice(df.index, 40), '评分'] = np.nan
df.loc[np.random.choice(df.index, 30), '配送时间'] = np.nan
# 制造异常值
df.loc[np.random.choice(df.index, 10), '销量'] = np.nan
df.loc[np.random.choice(df.index, 5), '配送时间'] = 999

import matplotlib.pyplot as plt

# 设置中文（防乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print('数据保存'+'-'*30)
df.to_csv('外卖脏数据.csv')

#read_csv这个函数是pandas的要带上前缀
df_new = pd.read_csv('外卖脏数据.csv')

print('数据清洗'+'-'*30)
df_new.head()

df_new.describe()

df_new.info()
print('已查询完毕数据基本内容')

#这个其实跟上面的info差不多了
df_new.isnull().sum()
print('已经检查完毕数据缺失值')

df_new['评分'] = df_new['评分'].fillna(df_new['评分'].mean())
df_new['配送时间'] = df_new['配送时间'].fillna(df_new['配送时间'].mean())
print('已经用每列平均值填充 评分 和 配送时间 的缺失值。')

#dropna(subset=['销量']) 会只删除“销量”这一列里是缺失值的行，其他列不受影响
df_new.dropna(subset=['销量'], inplace=True)
print('已删除销量缺失的行')
df_new.info()

#这种写法容易产生歧义
# df_new.replace(df_new['配送时间']>120,df_new['配送时间'].mean(), inplace=True)
mean_time = df_new['配送时间'].mean()
df_new.loc[df_new['配送时间'] > 120, '配送时间'] = mean_time
print('已用配送时间平均替换配送时间异常多的数据')

df_new.head()

print('店铺分析'+'-'*30)
merchant_df = df_new.groupby('店铺').agg({'销量':'sum','评分':'mean'})
merchant_df.rename(columns={'销量':'总销量'}, inplace=True)
print(merchant_df)

#ascending上升的
merchant_df.sort_values(by='总销量', ascending=False, inplace=True)
print(merchant_df)
print('已将结果按总销量从高到低排序，并打印')

print('准备开始进行可视化操作'+'-'*30)
#pd.to_datetime 是把 日期 列从字符串格式转成真正的日期类型
df_new['日期'] = pd.to_datetime(df_new['日期'])
#.dt.dayofweek 再从这个日期类型里提取出星期几
#默认情况下，.dt.dayofweek 返回的数字是：0代表周一，1代表周二，以此类推，6代表周日
df_new['星期'] = df_new['日期'].dt.dayofweek

#因为 agg('sum') 返回的是 Series，它的索引用 .index
df_new.groupby('星期')['销量'].agg('sum')

print('正式开始画图'+'-'*30)
fig, axes = plt.subplots(1,2,figsize=(12, 5))

axes[0].plot(df_new.groupby('星期')['销量'].agg('sum').index,df_new.groupby('星期')['销量'].agg('sum').values, color='blue', marker='o')
axes[0].set_ylabel('总销量')
axes[0].set_title('一周内销量变化趋势')

print('开始画第二个图'+'-'*30)
#统计每个状态的数量，用 size() 或 count() 就行
order_status_count = df_new.groupby('订单状态').size()
axes[1].pie(order_status_count.values, labels=order_status_count.index, autopct='%1.1f%%')
axes[1].set_title('订单状态占比')
#作用是把饼图的 y 轴标签清空
#不加上这行，画出来的图右边会显示一个没意义的 ylabel，比如“订单状态”之类的文字
plt.ylabel('')  # 饼图不需要y轴标签
plt.show()

print('图片已生成完毕')
print('本次数据分析已结束'+'-'*30)


import pandas as pd
import matplotlib.pyplot as plt
#%%
# 设置中文（防乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#%%
print('开始读取数据并进行检查数据'+'-'*100)
#%%
df = pd.read_csv('tmall_order_report.csv')
#%%
print(df.shape)
#%%
df.info()
#%%
df.head()
#%%
df.isnull().sum()
#%%
print('判断总金额跟支付金额的关系')
df['总金额'].unique()
df['买家实际支付金额'].unique()
print('在这两行代码的输出中可以看出来，其实买家实际支付金额跟总金额的关系只是加减法的问题')
#%%
print('看一下订单创建时间是什么类型的')
print(type(df['订单创建时间']))
# 2020-02-21 00:00:00
#复制粘贴了时间之后发现中间有空格
#%%
print('开始对数据进行清洗'+'-'*100)
df.head()
#%%
print('去除所有列名的首尾空格')
df.columns = df.columns.str.strip()
#%%
print('因为可以确定有总金额就一定会付款，所以，就可以默认为订单付款时间跟订单创建时间相同')
#现在的写法是更安全的，相当于是变量赋值，以后建议多用
df['订单付款时间'] = df['订单付款时间'].fillna(df['订单创建时间'])
df.head()
#%%
#这个失误我要保留，主要是因为看前五行的数据是真的没法看出太大的错误，所以这次的错误是我没有看到足够的数据
# 导致的分析错误
# print('总金额没有为0的所以支付金额应该跟总金额一致')
# df['买家实际支付金额'] = df['总金额']

#%%
df.head()
print(df.columns)
#%%
# print('把订单创建时间给改成两列，订单创建日期跟订单创建时间')
# df["订单创建时间"] = df["订单创建时间"].str.split(" ").str[]
# df.head()
#这个想法现在已经在下面的代码中实现了
#%%
df['订单创建时间'] = pd.to_datetime(df["订单创建时间"])
df.insert(4,'订单创建日期',df["订单创建时间"].dt.date.values)
#%%
df['订单创建时间'] = df['订单创建时间'].dt.time
#%%
df.head()
#%%
df['订单付款时间'] = pd.to_datetime(df["订单付款时间"])
df.insert(6,'订单付款日期',df["订单付款时间"].dt.date.values)
df['订单付款时间'] = df['订单付款时间'].dt.time
df.head()
#%%
df.info()
#%%
print('开始分组分析'+'-'*100)
#%%
print('列举总金额在前十的地区')
#%%
area_amount_top10 = df.groupby('收货地址').agg({'总金额':'sum'}).sort_values('总金额', ascending=False).head(10)
print(area_amount_top10)
#%%
print('列举退款金额在前十的地区')
#%%
area_refund_amount_top10 = df.groupby('收货地址').agg({'退款金额':'sum'}).sort_values('退款金额', ascending=False).head(10)
print(area_refund_amount_top10)
#%%
print('开始可视化操作'+'-'*100)
#%%
fig, axes = plt.subplots(1, 2, figsize=(19, 14))
#%%
axes[0].bar(area_amount_top10.index, area_amount_top10['总金额'],color='#95A5A6')
axes[0].set_title('1.总消费金额在前十的地区')
axes[0].set_xlabel('城市');axes[0].set_ylabel('总金额')
axes[0].tick_params(axis='x', rotation=45)
#%%
axes[1].bar(area_refund_amount_top10.index,area_refund_amount_top10['退款金额'],color='#F39C12')
axes[1].set_title('2.总退款金额在前十的地区')
axes[1].set_xlabel('城市');axes[1].set_ylabel('总退款金额')
axes[1].tick_params(axis='x', rotation=45)
#%%
# 调整间距，防止重叠
plt.tight_layout()

plt.savefig('完整天猫数据分析报告.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ 分析完成！图片已生成。")

#%%
print('开始文字报告输出'+'-'*100)
#%%
with open('tmall_order.txt', 'w', encoding='utf-8') as f:
    f.write(f'天猫用户中消费量前十的城市有:\n{area_amount_top10.to_string()}\n')
    f.write(f'天猫用户中退款金额前十的城市有:\n{area_refund_amount_top10.to_string()}\n')
#%%
with open('tmall_order.txt', 'r', encoding='utf-8') as f:
    print(f.read())
#%%
with open('tmall_order.txt', 'a', encoding='utf-8') as f:
    f.write('由上面的数据分析可知，上海这个城市是消费量最大并且也是退货量最大的城市\n'
            '不妨大胆推测，在上海生活的人们，消费能力强，并且对于自己不喜欢或者有质量问题的商品敢于向商家退款\n'
            '虽然这看起来是一个无关紧要的事情，但可以显示出人们对自己权力的争取\n'
            '这一点，是值得夸赞的。')
#%%
print('文字报告输出完毕')
import pandas as pd
#%%
df = pd.read_excel('天猫数据_1月到11月.xlsx')
#%%
print('开始检查数据'+'-'*100)
df.head()
#%%
df.info()
#%%
df.describe()
#%%
df.isnull().sum()
#%%
#其实说实话有了info之后其实这个shape就显得很无关紧要了
df.shape
#%%
print('目前分析下来，预估凑单价里面有空值，预估凑单说明里面有空值，核心优惠规则、更多优惠规则、优惠标签、补贴金额、优质品牌标识都含有空值，现在的问题是先要把空值给解决掉')
#%%
df.head()
#%%
print('对于预估凑单价，没办法清洗，原因如下：\n'
      '1.不知道内部信息，无法获得计算预估凑单价的方法\n'
      '2.空值占比过多，没办法删除\n'
      '所以，跳过\n')
#%%
print('对于预估凑单说明，可以采取一个未知是否凑单的提示')
df['预估凑单说明'] = df['预估凑单说明'].fillna('未知是否凑单')
#%%
df.head()
#%%
print('现在即将处理，核心优惠规则，更多优惠规则，优惠标签\n'
      '对于核心优惠规则，更多优惠规则这两列，采取无优惠的填补形式\n'
      '对于优惠标签这一列，将根据邮费来进行对应的选择，是包邮或者未知\n'
      '原因如下：\n'
      '核心优惠规则，更多优惠规则既然是空值，那就可以默认为是无优惠\n'
      '优惠标签的这种填补方法则是因为在如今的电商市场形势下，绝大部分的电商都会选择包邮，'
      )
#%%
df[['核心优惠规则','更多优惠规则']] = df[['核心优惠规则','更多优惠规则']].fillna('无优惠')
# df['邮费'].apply(lambda x:df['优惠标签'].fillna('包邮') if x==0 df['优惠标签'].fillna('未知'else x!=0)
# df['优惠标签'] = df['优惠标签'].fillna('包邮')
#上面这两个写法都是错的：第一个写法是逻辑上的问题，相当于是定位会出问题
#然后第二种写法是相当于没有看清题意，下面会是以比较符合题意的写法
#%%
# & 这个符号相当于and只不过是另一种表示方法
#这两行的本质的底层逻辑是一样的
#(df['邮费'] == 0) & (df['优惠标签'].isna())这个东西是按道理会返回bool类型，
# 但是在这里直接定位到行标签
#整体的底层原理是定位元素覆盖旧元素
df.loc[(df['邮费'] == 0) & (df['优惠标签'].isna()), '优惠标签'] = '包邮'
df.loc[(df['邮费'] != 0) & (df['优惠标签'].isna()), '优惠标签'] = '未知'
#%%
print('关于补贴金额，就按照正常的平均值来处理')
#%%
df['补贴金额'] = df['补贴金额'].fillna(df['补贴金额'].mean())
#%%
df.info()
#%%
#我这样写是我想用不完全归纳法判断是不是优质品牌标识都是0或者1，
# 但是在写完后我发现可以用if条件判断和for循环来判断（但是现在for循环又太慢了）
#所以我查了些信息发现pandas里面有更方便的
print('先用不完全归纳法判断  优质品牌标识  这一列都有哪些值')
df['优质品牌标识'].head(20)
print('前20列可以确定有1，0，nan  但是这样或许会有误差，可以用pandas里面的方法')
print('查看该列有哪些唯一值')
print(df['优质品牌标识'].unique())
print('确定只有0，1，nan')
#%%
print('现在的情况是确定了优质品牌标识里面的唯一值，但是没有具体的填充标准，所以说我做出的决定是不做任何填充')
#%%
print('数据清洗完毕，开始进行数据处理'+'-'*100)
df.head()
#%%
print('数据处理'+'-'*100)
#%%
df_Discounted_price = df.sort_values(by='折后价', ascending=False)
df_Discounted_price.head()
#%%
print('开始进行画图'+'-'*100)
#%%
df.groupby('所属品类')['补贴金额'].agg('sum')
#%%
import matplotlib.pyplot as plt
# 设置中文（防乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#%%
fig, axes = plt.subplots(figsize=(14, 10))
#%%
axes.bar(df.groupby('所属品类')['补贴金额'].agg('sum').index,df.groupby('所属品类')['补贴金额'].agg('sum').values, color='blue')
axes.set_title('品类与补贴金额的关系')
axes.set_xlabel('所属品类');axes.set_ylabel('总补贴金额')
#%%
plt.savefig('天猫分析报告.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ 分析完成！图片已生成。")

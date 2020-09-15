import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# 设置风格
sns.set(style='white', font_scale=1.2)
# matplotlib inline
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.unicode_minus']=False
import warnings
warnings.filterwarnings("ignore")

filename = "F:\111\信息数据源 .csv"
data = pd.read_csv(filename,encoding="gbk")
data.head()

# 根据业务需要提取数据，发货日期早于下单日期
# 1)转换时间类型
data["OrderDate"] = pd.to_datetime(data["OrderDate"])
data["ShipDate"] = pd.to_datetime(data["ShipDate"])
# 2)计算时间差
data["interval"] = (data["ShipDate"]-data["OrderDate"]).dt.total_seconds()
# 3)找时间差为负的数据并删除
data.drop(index=data[data["interval"]<0].index,axis=0,inplace=True)
print(data.shape)

# 查看行列数量
data.shape
# 数据整体描述
data.describe()
# 数据信息
data.info()
# 统计NAN数据
data.isna().sum()

# 重复值
print(data["RowID"].unique().size)
data[data["RowID"].duplicated()]
data.drop(index=data[data["RowID"].duplicated()].index,axis=0,inplace=True)
print(data.shape)

data[data["ShipMode"].isnull()]
data["ShipMode"].unique()
# 众数填充缺失值
# data["ShipMode"].mode()
data["ShipMode"].fillna(data["ShipMode"].mode()[0],inplace=True)

data[data["Discount"]>1]
data[data["Discount"]<0]
data["Discount"] = data["Discount"].mask(data["Discount"]>1,None)
# 处理缺失值
data["Discount"].isna().sum()
# 平均折扣
meanDiscount = data["Discount"].mean()
# data[data["Discount"].notnull()]["Discount"].sum()/data[data["Discount"].notnull()]["Discount"].size
data["Discount"].fillna(meanDiscount,inplace=True)

data.drop(columns=["PostalCode"],inplace=True)

data["Order-year"] = data["OrderDate"].dt.year
data["Order-month"] = data["OrderDate"].dt.month
data["quarter"] = data["OrderDate"].dt.to_period('Q')
data[["OrderDate","Order-year","Order-month","quarter"]].sample(5)

sales_year = data.groupby(by='Order-year')['Sales'].sum()
# print(sales_year)

sales_rate_12 = sales_year[2012] / sales_year[2011] - 1
sales_rate_13 = sales_year[2013] / sales_year[2012] - 1
sales_rate_14 = sales_year[2014] / sales_year[2013] - 1
# print(sales_rate_12,sales_rate_13,sales_rate_14)

sales_rate_12_label = "%.2f%%" % (sales_rate_12 * 100)
sales_rate_13_label  = "%.2f%%" % (sales_rate_13 * 100)
sales_rate_14_label  = "%.2f%%" % (sales_rate_14 * 100)
# print(sales_rate_12,sales_rate_13,sales_rate_14)

sales_rate = pd.DataFrame(
    {'sales_all':sales_year,
     'sales_rate':[0,sales_rate_12,sales_rate_13,sales_rate_14],
     'sales_rate_label':['0.00%',sales_rate_12_label,sales_rate_13_label,sales_rate_14_label]
    })
# print(sales_rate)

sales_rate = pd.DataFrame(
    {'sales_all':sales_year,
     'sales_rate':[0,sales_rate_12,sales_rate_13,sales_rate_14]
    })
y1 = sales_rate['sales_all']
y2 = sales_rate['sales_rate']
x = [str(value) for value in sales_rate.index.tolist()]
# 新建figure对象
fig=plt.figure(figsize=(10,6))
# 新建子图1
ax1=fig.add_subplot(1,1,1)
# ax2与ax1共享X轴
ax2 = ax1.twinx()
ax1.bar(x,y1,color = 'dodgerblue')
ax2.plot(x,y2,marker='o',color = 'r')
ax1.set_xlabel('年份')
ax1.set_ylabel('销售额')
ax2.set_ylabel('增长率')
ax1.set_title('销售额与增长率')

sales_area = data.groupby(by="Market")["Sales"].sum()
# sales_area
pie_labels = sales_area.index.to_list()
f, ax = plt.subplots(figsize=(10,10))
pie_sales_area = plt.pie(sales_area,labels=pie_labels,autopct="%.1f%%",startangle=90)
plt.title('2011-2014年总销售额占比')

# 各地区每一年的销售额
sales_area = data.groupby(by=["Market","Order-year"])["Sales"].sum()
# 将多层索引设置为列，level这个参数的意思是要把哪些索引设置为列
sales_area = sales_area.reset_index(level=[0,1])
# pd.pivot_table(data=sales_area,values="Sales",index="Market",columns="Order-year",aggfunc="sum")
# 绘制柱形图
fig = plt.figure(figsize=(10,6))
sns.barplot(x="Market",y="Sales",hue="Order-year",data=sales_area,estimator=np.sum)
plt.title('2011-2014年不同地区销售额对比')

# 各地区不同产品的销售额
sales_area = data.groupby(by=["Market","Category"])["Sales"].sum()
# 将多层索引设置为列，level这个参数的意思是要把哪些索引设置为列
sales_area = sales_area.reset_index(level=[0,1])
# pd.pivot_table(data=sales_area,values="Sales",index="Market",columns="Order-year",aggfunc="sum")
# 绘制柱形图
fig = plt.figure(figsize=(10,6))
sns.barplot(x="Market",y="Sales",hue="Category",data=sales_area,estimator=np.sum)
plt.title('不同产品类型在不同地区的销售额对比')

data_customer = data.copy()
data_customer = data_customer.drop_duplicates(subset=["CustomerID"])
new_customer = data_customer.groupby(["Order-year","Order-month"]).size()
new_customer = new_customer.reset_index(level=[0,1])
new_customer.columns = ["Order-year","Order-month","count"]
new_customer = pd.pivot_table(data=new_customer,values="count",index="Order-month",columns="Order-year",fill_value=0)
new_customer

# 获取2014年数据
data_14 = data [data ['Order-year']==2014]
data_14 = data_14[['CustomerID','OrderDate','Sales']]
# print(data_14.shape)
customdf = data_14.copy()
customdf.set_index('CustomerID',drop=True,inplace=True)
customdf['orders'] = 1
customdf
rfmdf = customdf.pivot_table(index=['CustomerID'],
                    values=['OrderDate','orders','Sales'],
                    aggfunc={'OrderDate':'max',
                            'orders':'sum',
                            'Sales':'sum'})

rfmdf['R'] = (rfmdf["OrderDate"].max()-rfmdf["OrderDate"]).dt.days
rfmdf.rename(columns={'Sales':'M','orders':'F'},inplace=True)
rfmdf

def rfm_func(x):
    level = x.apply(lambda x: "1" if x >= 0 else '0')
    label = level.R + level.F + level.M
    d = {
        '011':'重要价值客户',
        '111':'重要唤回客户',
        '001':'重要深耕客户',
        '101':'重要挽留客户',
        '010':'潜力客户',
        '110':'一般维持客户',
        '000':'新客户',
        '100':'流失客户'
    }
    result = d[label]
    return result

rfmdf['label'] = rfmdf[['R','F','M']].apply(lambda x:x-x.mean()).apply(rfm_func,axis=1)
rfmdf
result = rfmdf.groupby('label')["OrderDate"].count()
result = result.reset_index()
result.columns = ["label","count"]
result
# 绘制柱形图
fig = plt.figure(figsize=(10,6))
order = ['重要价值客户', '重要唤回客户', '重要深耕客户', '重要挽留客户', '潜力客户', '一般维持客户', '新客户', '流失客户']
sns.barplot(x="count",y="label",data=result,orient='h',order=order)
plt.title('RFM用户数')

rfm_score_df = rfmdf[['R','F',"M"]]
# 修改describe区间范围，得到五分位数
rfm_score_df.describe(percentiles=[0.2,0.4,0.6,0.8])

# 区间( ],所以第一个设置为最小值-1
section_list_R = [-1,9,24,43,103,362]
grade_R = pd.cut(rfm_score_df['R'],bins=section_list_R,labels=[5,4,3,2,1])
rfm_score_df['R_S'] = grade_R.values.astype(int)

# 区间( ],所以第一个设置为最小值-1
section_list_F = [0,4,7,13,19,48]
grade_F = pd.cut(rfm_score_df['F'],bins=section_list_F,labels=[1,2,3,4,5])
rfm_score_df['F_S'] = grade_F.values.astype(int)

# 区间( ],所以第一个设置为最小值-1
section_list_M = [0,365,1196,2855,4938,23296]
grade_M = pd.cut(rfm_score_df['M'],bins=section_list_M,labels=[1,2,3,4,5])
# 上一步的cut方法返回值是category类型，不能用户后续计算，这里要转为数值类型
rfm_score_df['M_S'] = grade_M.values.astype(int)
rfm_score_df

def rfm_func(x):
    level = x.apply(lambda x: "1" if x >= 0 else '0')
    level
    label = level.R_S + level.F_S + level.M_S
    d = {
        '111':'重要价值客户',
        '011':'重要唤回客户',
        '101':'重要深耕客户',
        '001':'重要挽留客户',
        '110':'潜力客户',
        '010':'一般维持客户',
        '100':'新客户',
        '000':'流失客户'
    }
    result = d[label]
    return result

rfm_score_df["label"] = rfm_score_df[["R_S","F_S","M_S"]].apply(lambda x:x-x.mean()).apply(rfm_func,axis=1)
rfm_score_df
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv('Profit by product - 202001-202102.csv')

df=df.groupby(by='Product Type').sum()
df['Profit Margin(%)']=df['Gross Profit']/df['Net Sales']*100
df=df[['Quantity','Net Sales', 'Gross Profit','Profit Margin(%)']]
df=df.drop(['Default','simple','variable'],axis=0)
df['Net Sales (%)']=df['Net Sales']/df['Net Sales'].sum()*100
df['Gross Profit (%)']=df['Gross Profit' ]/df['Gross Profit' ].sum()*100
df=df[['Quantity','Net Sales','Net Sales (%)', 'Gross Profit','Gross Profit (%)','Profit Margin(%)']]
df.to_excel('Sales_Profits_onlinestore.xlsx')


branch_sales=pd.read_excel('PM2ND sales by products - 202001-202102.xlsx',skiprows=2)
branch_dept=pd.read_excel('Products by Department - branch.xlsx',skiprows=3)
branch_cost=pd.read_excel(r'ks.xlsx',skiprows=2)
branch_sales=branch_sales[['Product Number','Quantity', 'Sales Amount']]
branch_dept=branch_dept[['Product Num','Department']]
branch_cost=branch_cost[['Product Number','Unit Cost']]
c_merged=branch_sales.merge(branch_cost,how='left',on='Product Number')
c_merged['Cost']=c_merged['Unit Cost']*c_merged['Quantity']
c_merged=c_merged.drop('Unit Cost',axis=1)
c_merged['Profit']=c_merged['Sales Amount']-c_merged['Cost']
c_merged=c_merged.drop('Cost',axis=1)
c_merged=c_merged.merge(branch_dept,how='left',left_on='Product Number',right_on='Product Num')
c_merged=c_merged.drop('Product Num',axis=1)
c_merged=c_merged.groupby(by='Department').sum()
sales_sum=c_merged['Sales Amount'].sum()
profit_sum=c_merged['Profit'].sum()
profit_margin_sum=float(profit_sum)/sales_sum*100
c_merged=c_merged[(c_merged.index=='APPLIANCES')|(c_merged.index=='BEAUTY')|(c_merged.index=='HOUSEHOLD')|(c_merged.index=='KITCHEN')|(c_merged.index=='KITCHEN ')]
c_merged.loc['LIFE']=c_merged.iloc[2:5,:].sum()
c_merged['Profit Margin(%)']=c_merged['Profit']/c_merged['Sales Amount']*100
c_merged=c_merged.drop(['HOUSEHOLD','KITCHEN','KITCHEN '],axis=0)
c_merged['Sales Amount (%)']=c_merged['Sales Amount']/c_merged['Sales Amount'].sum()*100
c_merged['Profit (%)']=c_merged['Profit']/c_merged['Profit'].sum()*100
c_merged=c_merged[['Quantity','Sales Amount','Sales Amount (%)','Profit','Profit (%)','Profit Margin(%)']]

c_merged.to_excel('Sales_Profits_pm2nd.xlsx')

x=range(len(df))

fig=plt.figure()
fig.set_size_inches(10,18)
ax=fig.add_subplot(211)
ax2=ax.twinx()
ax.bar([i-0.2 for i in x],df['Profit Margin(%)'],width=0.2,color='red',label='Profit Margin(%)')
ax2.bar([i for i in x],df['Net Sales'],width=0.2,color='green',label='Net Sales')
ax2.bar([i+0.2 for i in x],df['Gross Profit'],width=0.2,color='blue',label='Gross Profit')
ax.set_ylabel('Percentage')
ax2.set_ylabel('Sales Amount')
ax.set_ylim(0,100)
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.set_xticks(x)
ax2.set_xticks(x)
ax.set_xticklabels(df.index,rotation=45)
ax2.set_xticklabels(df.index,rotation=45)
ax.title.set_text('Online Store Sales - 2020')

y=range(len(c_merged))
ax_c=fig.add_subplot(212)
ax_c2=ax_c.twinx()
ax_c.bar([i-0.2 for i in y],c_merged['Profit Margin(%)'],width=0.2,color='red',label='Profit Margin(%)')
ax_c2.bar([i for i in y],c_merged['Sales Amount'],width=0.2,color='green',label='Net Sales')
ax_c2.bar([i+0.2 for i in y],c_merged['Profit'],width=0.2,color='blue',label='Gross Profit')
ax_c.set_ylabel('Percentage')
ax_c2.set_ylabel('Sales Amount')
ax_c.set_ylim(0,100)
ax_c.legend(loc='upper left')
ax_c2.legend(loc='upper right')
ax_c.set_xticks(y)
ax_c2.set_xticks(y)
ax_c.set_xticklabels(c_merged.index,rotation=45)
ax_c2.set_xticklabels(c_merged.index,rotation=45)
ax_c.title.set_text('KS Sales - 2020')
fig.tight_layout()
print(df)
print(c_merged)
print('PM2ND Profit Margin: '+str(profit_margin_sum)+'%')
plt.show()
'''
fig=plt.figure()
fig.set_size_inches(10,18)
ax=fig.add_subplot(211)
ax2=ax.twinx()
ax.bar([i-0.2 for i in x],df['Profit Margin(%)'],width=0.2,color='red',label='Profit Margin(%)')
ax2.bar([i for i in x],df['Net Sales (%)'],width=0.2,color='green',label='Net Sales (%)')
ax2.bar([i+0.2 for i in x],df['Gross Profit (%)'],width=0.2,color='blue',label='Gross Profit (%)')
ax.set_ylabel('Percentage')
ax2.set_ylabel('Percentage')
ax.set_ylim(0,100)
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.set_xticks(x)
ax2.set_xticks(x)
ax.set_xticklabels(df.index,rotation=45)
ax2.set_xticklabels(df.index,rotation=45)
ax.title.set_text('Online Store Sales - 202001-202102')

y=range(len(c_merged))
ax_c=fig.add_subplot(212)
ax_c2=ax_c.twinx()
ax_c.bar([i-0.2 for i in y],c_merged['Profit Margin(%)'],width=0.2,color='red',label='Profit Margin(%)')
ax_c2.bar([i for i in y],c_merged['Sales Amount (%)'],width=0.2,color='green',label='Net Sales (%)')
ax_c2.bar([i+0.2 for i in y],c_merged['Profit (%)'],width=0.2,color='blue',label='Gross Profit (%)')
ax_c.set_ylabel('Percentage')
ax_c2.set_ylabel('Percentage')
ax_c.set_ylim(0,100)
ax_c.legend(loc='upper left')
ax_c2.legend(loc='upper right')
ax_c.set_xticks(y)
ax_c2.set_xticks(y)
ax_c.set_xticklabels(c_merged.index,rotation=45)
ax_c2.set_xticklabels(c_merged.index,rotation=45)
ax_c.title.set_text('PM2ND Sales - 202001-202102')
fig.tight_layout()
print(df)
print(c_merged)
print('PM2ND Profit Margin: '+str(profit_margin_sum)+'%')
plt.savefig('img.png')
'''

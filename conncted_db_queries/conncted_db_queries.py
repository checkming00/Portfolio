import pymssql
from sqlalchemy import create_engine
import pandas as pd


#UserName and password shielded
engine=create_engine('mssql+pymssql://username:password@ZM/MBPOSDB',echo=True)
con=engine.connect()


def inventory23():
    #Query inventory information and save as an Excel file
    df=pd.read_sql('select i.Prod_Num,i.Bin,p.Barcode,p.Prod_Name,p.Prod_Alias,p.Measure,i.Quan_On_Hand from dbo.Inventory as i left join dbo.Product as p on i.Prod_Num=p.Prod_Num',con)
    df=df.rename(columns={'Prod_Num':'Product Number','Bin':'Bin/  Location','Prod_Name':'Product Name','Prod_Alias':'Product Alias','Measure':'Measurement','Quan_On_Hand':'Qty.       On Hand'})
    df.to_excel('data.xlsx',index=False)
 
def purchase23(start_date,end_date):
    #Query purchase information by vendors of a date range inputted and save as an Excel file
    df=pd.read_sql(
        '''
        select VenNum,VenName,sum(Sub_Total) as Sub_Total,sum(Freight) as Freight,
        sum(Miscellanea) as Miscellanea,sum(Tax1) as Tax1,
        sum(Tax2) as Tax2,sum(Discount) as Discount,
        sum(Grand_Total) as Grand_Total
        from dbo.PurchaseOrder
        where CreateDate>='{sd}' and CreateDate<='{ed}'
        group by VenNum,VenName
        order by sum(Grand_Total) desc'''.format(sd=start_date,ed=end_date),con)
    df.to_excel(r'Z:\Ben\Small Program\query\purchase23.xlsx',index=False)


def sales23(start_date,end_date):
    #Query sales information by customers of a date range inputted and save as an Excel file
    df=pd.read_sql(
        '''
        select co.Cust_Num,c.Cust_Name,sum(co.Sub_Total) as Sub_Total,
        sum(co.Tax1) as Tax1,sum(co.Tax2) as Tax2,sum(co.Discount_Amount) as Discount,
        sum(co.Total_Amount) as Total_Amount
        from Cust_Order as co
        left join Customer as c
        on co.Cust_Num=c.Cust_Num
        where co.Date_Enter>='{sd}' and co.Date_Enter<='{ed}'
        group by co.Cust_Num,c.Cust_Name
        order by sum(co.Total_Amount) desc'''.format(sd=start_date,ed=end_date),con)
    df.to_excel(r'Z:\Ben\Small Program\query\sales23.xlsx',index=False)

def products_by_vendor(vendor):
    #Query products information by the vendor inputted and save as an Excel file
    df=pd.read_sql(
        '''
        select distinct pi.ProdNum,po.VenName from Purchase_Item as pi
        left join PurchaseOrder as po
        on pi.PurchNum=po.PurchNum
        where po.VenNum='{vendor}'
        '''.format(vendor=vendor),con)
    df.to_excel(r'Z:\Ben\Small Program\query\products_by_'+vendor+'.xlsx',index=False)


def products_by_dept(dept):
    #Query products infomation by the department inputted and save as an Excel file
    df=pd.read_sql(
        '''
        select distinct pi.ProdNum,p.Department,po.VenName from Purchase_Item as pi
        left join PurchaseOrder as po
        on pi.PurchNum=po.PurchNum
        left join Product as p
        on pi.ProdNum=p.Prod_Num
        where p.Department='{dept}'
        '''.format(dept=dept),con) 
    df.to_excel(r'Z:\Ben\Small Program\query\products_by_'+dept+'.xlsx',index=False)

def product_move(PN):
    #Query the product inputted to display all the moves including purchase, return,
    #selling, credit, transferral and adjustment and save as an Excel file.
    df1=pd.read_sql(
        '''select ri.Prod_Num as PN,ri.Rec_Qty as QTY,r.Rec_Date as Date,r.Ven_Name as VC_Name
        from Receive_Item as ri
        left join Receive as r
        on ri.Rec_Num=r.Rec_Num
        where ri.Prod_Num='{PN}'
        '''.format(PN=PN),con)

    df2=pd.read_sql('''select ii.Prod_Num as PN,ii.Ship_Quantity as QTY,i.Date_Sent as Date,c.Cust_Name as VC_Name
        from Invoice_Item as ii
        left join Invoice as i
        on ii.Invoice_Num=i.Invoice_Num
        left join Customer as c
        on i.Cust_Num=c.Cust_Num
        where i.Void_Invoice=0 and ii.Prod_Num='{PN}'
        '''.format(PN=PN),con)
        
    df3=pd.read_sql('''select ti.Prod_Num as PN,ti.Qty as QTY,t.TxnDate as Date,t.ToSiteId as VC_Name
        from TransferStock_Item as ti
        left join TransferStock as t
        on ti.TxnId=t.TxnId
        where t.FromSiteId='Toronto' and ti.Prod_Num='{PN}'
        union all
        select ti.Prod_Num as PN,ti.Qty as QTY,t.TxnDate as Date,t.FromSiteId as VC_Name
        from TransferStock_Item as ti
        left join TransferStock as t
        on ti.TxnId=t.TxnId
        where t.ToSiteId='Toronto' and ti.Prod_Num='{PN}'
        '''.format(PN=PN),con)

    df4=pd.read_sql('''select ProdNum as PN,(NewQty-OldQty) as QTY,DateAdj as Date,Reason as VC_Name
        from InventoryAdjust
        where Reason not like 'Receive%' and ProdNum='{PN}'
        '''.format(PN=PN),con)
    df1['TYPE']='Received'
    df2['TYPE']=df2['QTY'].apply(lambda x:'Invoice' if x>=0 else 'Credit')
    df2['QTY']=df2['QTY']*(-1)
    df3['TYPE']=df3['QTY'].apply(lambda x:'Transfer Out' if x<=0 else 'Transfer In')
    df4['TYPE']='Adjustment'
    df=pd.concat([df1,df2,df3,df4],ignore_index=True)
    df=df.sort_values(by=['Date'])
    df['CumSum']=df['QTY'].cumsum()
    df.to_excel(r'Z:\Ben\Small Program\query\product_move.xlsx',index=False)
 
        

def check_table(table):
    #Simply look at columns of a table inputted 
    columns=pd.read_sql(
        '''
        select *
        from {table}'''.format(table=table),con).columns
    print(table+"'s columns:")
    print(columns)


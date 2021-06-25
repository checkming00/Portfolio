import pandas as pd
from datetime import datetime

payroll=pd.read_excel('payroll.xlsx')

#Add a column as utilization rate
utill_rate_ls=[]
for i,row in payroll.iterrows():
    if row['Payroll_Hours']==0:
        utill_rate_ls.append(0)
    else:
        ur=round((row['Billed_Hours']+row['Cancelled_Hours'])/row['Payroll_Hours']*100,2)
        utill_rate_ls.append(ur)
payroll['Utilization_Rate(%)']=utill_rate_ls

#Drop "Unique_Circumsta" outliers and the job which is not "RBT" or "BCBA"
payroll=payroll[(pd.isna(payroll['Unique_Circumsta']))&((payroll['Job']=='OCC')|(payroll['Job']=='1O1'))]

#Aggregate utilization rate by mean and Group by Job
utill_rate_by_job=payroll.groupby('Job')['Utilization_Rate(%)'].mean()
utill_rate_by_job=utill_rate_by_job.reset_index()
utill_rate_by_job['Utilization_Rate(%)']=utill_rate_by_job['Utilization_Rate(%)'].apply(lambda x:round(x,2))

#Add the target column for comparation
utill_rate_by_job['Target']=utill_rate_by_job['Job'].apply(lambda x:90 if x=='1O1' else 60)

#Add the comparation columns
utill_rate_by_job['Diff']=utill_rate_by_job['Utilization_Rate(%)']-utill_rate_by_job['Target']
utill_rate_by_job['Diff_Rate(%)']=round(utill_rate_by_job['Diff']/utill_rate_by_job['Target']*100,2)
print(utill_rate_by_job)
utill_rate_by_job.to_excel('overall.xlsx',index=False)
# -- This is done for Part 2 1.a --

#Add a column as start date cohort using "YYYY-mm" format
payroll['Start_Date_Cohort']=payroll['Start_Date'].apply(lambda x:datetime.strftime(x,'%Y-%m'))

#Export a clean and ready-to-use Excel file for visualization
payroll.to_excel('payroll_cleaned.xlsx',index=False)


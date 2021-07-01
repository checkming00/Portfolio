import pandas as pd
import os

path=os.path.abspath(os.path.join(os.getcwd(),".."))

death=pd.read_csv(path+'\\covid_deaths.csv',
                  usecols=['continent','location','date','population','total_cases','total_deaths'],
                  parse_dates=['date'])

death=death[~pd.isna(death['continent'])]

vaccine=pd.read_csv(path+'\\covid_vaccinations.csv',
                    usecols=['continent','location','date','people_vaccinated','people_fully_vaccinated'],
                    parse_dates=['date'])

vaccine=vaccine[~pd.isna(vaccine['continent'])]

merged=death.merge(vaccine,how='inner',on=['continent','location','date'])
merged=merged.sort_values(by=['location','date'])

countries=list(merged['location'].unique())

def handle_na(df,col):
    if pd.isna(df[col][0]):
        df[col][0]=0
        merged[col][df['index'][0]]=0
    for i in range(1,len(df)):
        if pd.isna(df[col][i]):
            df[col][i]=df[col][i-1]
            merged[col][df['index'][i]]=df[col][i]

for country in countries:
    c=merged[merged['location']==country]
    c.reset_index(drop=False,inplace=True)
    handle_na(c,'people_vaccinated')
    handle_na(c,'people_fully_vaccinated')

merged=merged.fillna(0)

merged.to_csv(path+'\\death_vaccine_cleaned.csv',index=False)

last_date=merged.groupby('location').max()
last_date.to_csv(path+'\\last_date.csv')

total=pd.DataFrame({'population':[int(last_date['population'].sum())],
                    'total_cases':[int(last_date['total_cases'].sum())],
                    'people_vaccinated':[int(last_date['people_vaccinated'].sum())],
                    'people_fully_vaccinated':[int(last_date['people_fully_vaccinated'].sum())]})

total.to_csv(path+'\\global_vaccinations.csv',index=False)

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def getHTMLText(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""


def getInfo(url):
    d=dict()
    html=getHTMLText(url)
    soup=BeautifulSoup(html,'html.parser')
    meta=soup.find('meta',{'id':'MetaSchoolAddress'})
    address=meta.get('content')
    meta=soup.find('meta',{'id':"MetaSchoolPhone"})
    phone=meta.get('content')
    d['address']=address
    d['phone']=phone
    return d



df=pd.read_excel('OA_info.xlsx')
df['Address']=df['URL'].apply(lambda x:getInfo(x)['address'])
df['Phone']=df['URL'].apply(lambda x:getInfo(x)['phone'])
df.to_excel('OA2.xlsx',index=False)

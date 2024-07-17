import pandas as pd
import numpy as np


def preprocess(df,noc):
    df=df[df['Season']=='Summer']
    df=df.merge(noc,on='NOC',how='left')
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)
   
    return df
def year_country(df):
    a=df['Year'].unique().tolist()
    a.sort()
    a.insert(0,'overall')
    b=df['region'].dropna().unique().tolist()
    b.sort()
    b.insert(0,'overall')
    return a,b 

import pandas as pd
import seaborn as sns
def medal_tally(df,year,country):
    if year!='overall':
        df=df[df['Year']==year]
    if country!='overall':
        df=df[df['region']==country]
    #it s showing wrong result because if gautam garg gaurav garg are hockey player anmd hockey team won gold in 1996 then 
    #2 gold are counted for them if 11 players are there the 11 gold for 1 match are counted lets correct that 
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if year=='overall' and country!='overall':#this is because if year is overall the we want to show all years so we have to groupby with years
        medal_tally=medal_tally.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else: 
        medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    medal_tally['total']=medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    # medal_tally['Gold']=medal_tally['Gold'].astype(int)
    # medal_tally['Silver']=medal_tally['Silver'].astype(int)
    # medal_tally['Bronze']=medal_tally['Bronze'].astype(int)
    # medal_tally['Total']=medal_tally['Total'].astype(int)
    return medal_tally

def overall_analysis(df):

    editions=len(df['Year'].unique())
    cities=len(df['City'].unique())
    sports=len(df['Sport'].unique())
    atheletes=len(df['Name'].unique())
    participating_nations=len(df['region'].unique())
    events=len(df['Event'].unique())
    return editions,cities,sports,atheletes,participating_nations,events 
def partipated_countries_vs_year(df):
    # a=df.groupby(['Year'])['region'].unique().reset_index()
    # b=[]
    # for i in a['region']:
    #     # a['participated_nations']=len(i)
    #     b.append(len(i))
    # a['participated_nations']=b
    #the baove task can be done by 
    g=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values(['Year'])
    g.rename(columns={'count':'countries'},inplace=True)
    return g

def events_vs_year(df):
    gg=df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values(['Year'])
    gg.rename(columns={'count':'events'},inplace=True)
    return gg
def athelets_vs_year(df):
    ggg=df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values(['Year'])
    ggg.rename(columns={'count':'atheletes'},inplace=True)
    return ggg
def most_succesfull_athelete(df,sport):
    if sport!='overall':
        df=df[df['Sport']==sport]
    k=df.groupby('Name').sum()[['Gold','Bronze','Silver']].reset_index()
    k['total']=k['Gold'] + k['Silver'] + k['Bronze']
    k=k.sort_values(['total','Gold','Silver'],ascending=False)
    k.drop(columns=['Gold','Silver','Bronze'],inplace=True)
    new_df = df[['Name', 'Team', 'Sport','region']].copy()
    new_df=new_df.drop_duplicates(['Name'])
    k=pd.merge(new_df,k,on='Name')
    k=k.sort_values(['total'],ascending=False)
    return k

def country_level_most_successful(df,country):
    new_df=df[df['region']==country]
    new_df=df.dropna(subset=['Medal'])
    a=df.groupby(['Name']).count()['Medal'].reset_index().sort_values(['Medal'],ascending=False)
    return a 


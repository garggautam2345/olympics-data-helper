import streamlit as st
import pandas as pd 
import preprocessor,helper
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.figure_factory as ff   
df=pd.read_csv('athlete_events.csv')
noc=pd.read_csv('noc_regions.csv')
st.sidebar.title("olympics analysis")
st.sidebar.image('1.webp')
user_menu=st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country wise analysis','Athelete wise analysis')
)
df=preprocessor.preprocess(df,noc)
if user_menu=='Medal Tally':
     year_list,country_list=preprocessor.year_country(df)
     year=st.sidebar.selectbox('SELECT YEAR',options=year_list)
     country=st.sidebar.selectbox('Country',options=country_list)
     new_df=helper.medal_tally(df,year,country)

     if year=='overall' and country=='overall':
          st.title("showing overall analysis")
     if year=='overall' and country!='overall':
          st.title( country +"overall performence" )
     if year!='overall' and country=='overall':
          st.title("medal tally in " + str(year) + "olympics")
     if year!='overall' and country!='overall':
          st.title("showing analysis for " + " " +country +" " + "in" + " " + str(year))
     st.dataframe(new_df)
if user_menu=='Overall Analysis':
     st.title("TOP STATISTICS")
     col1,col2,col3=st.columns(3)
     editions,cities,sports,atheletes,participating_nations,events=helper.overall_analysis(df)
     with col1:
          st.title("editions")
          st.write(editions)
     with col2:
          st.title("cities")
          st.write(cities)
     with col3:
          st.title("sports")
          st.write(sports)
     with col1:
          st.title("atheletes")
          st.write(atheletes)
     with col2:
          st.title("nations")
          st.write(participating_nations)
     with col3:
          st.title("events")
          st.write(events)
     st.title("participatig nations over time")
     g=helper.partipated_countries_vs_year(df)
    #  fig,ax=plt.subplots()
    #  ax.plot(g['Year'],g['count'])
    #  ax.set_xlabel('Year')
    #  ax.set_ylabel('countries')
    #  st.pyplot(fig)
    #this kind of graph is not good because as we hover the graphwe are not getting the values at that point so we will use plotly
     fig=px.line(g,x='Year',y='countries')
     st.plotly_chart(fig)
    
    
     st.title("events over time")
     gg=helper.events_vs_year(df)
     fig=px.line(gg,x='Year',y='events')
     st.plotly_chart(fig)


     st.title("atheletes over time")
     ggg=helper.athelets_vs_year(df)
     fig=px.line(ggg,x='Year',y='atheletes')
     st.plotly_chart(fig)

     st.title('MOST SUCCESSFUL ATHELETE')
     sports_lsit=a=df['Sport'].unique().tolist()
     sports_lsit.sort()
     sports_lsit.insert(0,'overall')
     sport=st.selectbox("select the sport",options=sports_lsit)
     k=helper.most_succesfull_athelete(df,sport)
     st.dataframe(k.head(20))

     st.title("NUMBER OF EVENTS FOR EVERY SPORT IN EACH YEAR")
     x=df.drop_duplicates(['Year','Sport','Event'])
     fig,ax=plt.subplots(figsize=(20,20))
     ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
     st.pyplot(fig)

if user_menu=='Country wise analysis':
     new_df=df.dropna(subset=['Medal'])
     new_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
     country_list=new_df['region'].dropna().unique().tolist()
     country_list.sort()
     country=st.selectbox("select the country",options=country_list)
     new_df=new_df[new_df['region']==country]
     a=new_df.groupby(['Year']).count()['Medal'].reset_index()
     
     fig=px.line(a,x='Year',y='Medal')
     st.plotly_chart(fig)
     fig,ax=plt.subplots(figsize=(20,20))
     sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int),annot=True)
     st.pyplot(fig)
     
     st.title("MOST SUCCESSFUL ATHELETE OF " + country + "ARE")
     result=helper.country_level_most_successful(df,country)
     st.dataframe(result.head(10))

     atheletes_df=df.drop_duplicates(subset=['Name','region'])
     x1=atheletes_df['Age'].dropna()
     x2=atheletes_df[atheletes_df['Medal']=='Gold']['Age'].dropna()
     x3=atheletes_df[atheletes_df['Medal']=='Silver']['Age'].dropna()
     x4=atheletes_df[atheletes_df['Medal']=='Bronze']['Age'].dropna()
     fig=ff.create_distplot([x1,x2,x3,x4],["OVERALL AGE DISTRIBUTION","GOLD MEDALIST","SILVER MEDALIST","BRONZE MEDALIST"],show_hist=False,show_rug=False)
     st.plotly_chart(fig)
     
    



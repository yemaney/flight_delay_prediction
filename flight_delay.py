#%%
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


part = st.sidebar.radio(label='Parts', options=('Introduction', 'Analyze columns with a lot of null values', 
                                         'Flight Distance Analysis', 'Departure Delay Time Analysis',
                                         'Analysis of Categorical Variables of Interest', 'Final conclusions'))


df = pd.read_csv('flights_sample.csv', sep=';')
df['fl_date'] = pd.to_datetime(df['fl_date'], format='%Y-%m-%d')

#%%
if part == 'Introduction':
    st.title('Flight Delay Analysis')
    
    st.markdown('''
                ## Structure of Notebook
                1. Basic Data Introduction
                2. Analyze columns with a lot of null values
                3. Flight Distance Analysis
                4. Departure Delay Temporal Analysis
                5. Analysis of Categorical Variables of Interest
                6. Final conclusions
                ''')
    
    st.title('Basic Introduction')
 
    fig = px.histogram(data_frame=df, x='arr_delay')
    st.plotly_chart(fig, use_container_width=True)
    
#%%
    fig1 = px.box(data_frame=df, x='arr_delay')
    st.plotly_chart(fig1, use_container_width=True)   
# %%
    st.markdown('''
        ## Initial Data Introduction
        - Inital look at data tells us that flight delays are very skewed.
        - Majority of flights are expected to be early, or on time as the median fligth delay is `-6`
        - Although most flights make good time. Their seems to be a tendancy for extreme outliers.        
                ''')
#%%
elif part == 'Analyze columns with a lot of null values':
    
    st.title('Analyzing Coulmns With Many Nulls')
    
    null_columns = df.columns[df.isnull().sum() > 70000]
    null_columns = np.append(null_columns.values, np.array(['fl_date', 'arr_delay']))
    
    df_null = df[null_columns].copy(deep=True)
    df_null['month'] =  df_null.fl_date.dt.month
    df_null['week'] = df_null.fl_date.dt.isocalendar().week
    df_null['day'] = df_null.fl_date.dt.day_of_year
    df_null['arr_delay'] = df_null['arr_delay'].fillna(0)
    df_null['arr_delay_bool'] = df_null['arr_delay'] > 0
    
    col = ['carrier_delay', 'weather_delay', 'nas_delay',
       'security_delay', 'late_aircraft_delay', 'first_dep_time',
       'total_add_gtime', 'longest_add_gtime']

    fig1 = px.box(data_frame=df_null, x=col)
    st.plotly_chart(fig1, use_container_width=True)
    
#%%
    null_columns = df.columns[df.isnull().sum() > 70000]
    null_columns = np.append(null_columns.values, np.array(['fl_date', 'arr_delay']))

    df_null = df[null_columns].copy(deep=True)
    df_null['month'] =  df_null.fl_date.dt.month
    df_null['week'] = df_null.fl_date.dt.isocalendar().week
    df_null['day'] = df_null.fl_date.dt.day_of_year
    df_null['arr_delay'] = df_null['arr_delay'].fillna(0)
    df_null['arr_delay_bool'] = df_null['arr_delay'] > 0
    x= df_null.groupby(by=['month', 'cancellation_code'])['arr_delay_bool'].count().unstack()
    
    fig1 = px.bar(x, barmode='group', opacity=0.8)
    st.plotly_chart(fig1, use_container_width=True)

#%%
    
    col1, col2 = st.beta_columns(2)
    with col1:
        col = st.radio('Variable', ('carrier_delay', 'weather_delay', 'nas_delay',
       'security_delay', 'late_aircraft_delay'))
    with col2:
        period = st.radio('Time', ('month', 'week', 'day'))
        

    def analyze_null(period, col):
        scaler = StandardScaler()
        int_delay_num = pd.DataFrame(df_null.groupby(by=period)[col].agg(lambda x: (x > 0).sum()))
        int_delay_num = scaler.fit_transform(int_delay_num)
        
        scaler2 = StandardScaler()
        delay_total_num = pd.DataFrame(df_null.groupby(by=period)['arr_delay_bool'].sum())
        delay_total_num = scaler2.fit_transform(delay_total_num)
        
        scaler3 = StandardScaler()
        flight_per_period = pd.DataFrame(df_null.groupby(by=period)['fl_date'].count())
        flight_per_period = scaler3.fit_transform(flight_per_period)
        
        x = pd.DataFrame.from_dict(dict(int_delay_num=int_delay_num.reshape(-1,), 
                        delay_total_num=delay_total_num.reshape(-1,),
                        flight_per_period=flight_per_period.reshape(-1,)))
    
        fig = px.line(x)
        st.plotly_chart(fig)
    
    analyze_null(period, col)
#%%



    
    
    st.markdown('''
## Cancellation code
Seems to have some prediction power, particularly code B during the early and late months tends to correlate with more delays. 
- However, the meaning of the codes is not actually known by me, so interpretability is lost
- this project is concerned with predicting delays, and using cancellations as a predictor seems wrong now

## Null delays
These columns seem highly correlated with the number of arrivals delays.
- However, since over 80% of the values are missing:
    - At this point, any sort of average (mean, median, mode) would lose any meaning
- Imputing the missing values with zeros could make sense, as one could interpret missing entries as the flight not being delayed
    - However, the entries would still be very sparse, and would be no different than indicators of the time of the flights  
                ''')
# %%
elif part == 'Flight Distance Analysis':
    st.title('Analyzing Delays Based on Distance')
#%%    
    fig = px.histogram(data_frame=df, x='distance')
    st.plotly_chart(fig)
# %%
    df['distance_bins'] = pd.cut(df['distance'], 100)
    df['delay_bool'] = df['dep_delay'] > 0
    
    num_delays = df.groupby(by='distance_bins')['delay_bool'].sum().values
    num_flight = df.groupby(by='distance_bins')['delay_bool'].count().values

    x = pd.DataFrame.from_dict(dict(num_delays=num_delays.reshape(-1,), num_flight=num_flight.reshape(-1,)))
    
    fig = px.line(x)
    st.plotly_chart(fig)
# %%
    scale = MinMaxScaler()
    x = pd.DataFrame(df.groupby(by='distance_bins')['delay_bool'].sum())
    x = scale.fit_transform(x).reshape(-1,)

    scale2 = MinMaxScaler()
    y = pd.DataFrame(df.groupby(by='distance_bins')['delay_bool'].count())
    y = scale2.fit_transform(y).reshape(-1,)

    z = df.groupby(by='distance_bins')['delay_bool'].sum().values / df.groupby(by='distance_bins')['delay_bool'].count().values

    data = pd.DataFrame.from_dict(dict(x=x,y=y,z=z))
    
    fig= px.line(data)
    st.plotly_chart(fig)

# %%
    st.markdown('''
## Flight Distance Analysis: conclusion
- shorter flights have more delays than longer delays
- when flight traffic is considered
    - there is a slight between delays and distance
        - shorter flights experience more delays because shorter flights are more common
        - flight that have very large distances have sporadic proportions of flight delays
            - this is probably due to the fact that they are so rare               
                ''')

elif part == 'Departure Delay Time Analysis':
    st.title('Departure Delay Time Analysis')
#%% 
    df['delay_bool'] = df['dep_delay'] > 0    
    df['month'] =  df.fl_date.dt.month
    df['week'] = df.fl_date.dt.isocalendar().week
    df['day'] = df.fl_date.dt.day_of_year
    df['day_of_week'] = df.fl_date.dt.dayofweek
    df['hour'] = pd.cut(df['dep_time'], bins=24)
    
    period = st.radio('Period', ('month', 'week', 'day', 'day_of_week'))
#%%
    def analyze_period(period):
        scaler = StandardScaler()
        x = pd.DataFrame(df.groupby(by=period)['fl_date'].count())
        x = scaler.fit_transform(x)
        x = x.reshape(-1,)
        
        scaler2 = StandardScaler()
        y = pd.DataFrame(df.groupby(by=period)['dep_delay'].mean())
        y = scaler2.fit_transform(y)
        y = y.reshape(-1,)
        
        data = pd.DataFrame.from_dict(dict(x=x, y=y))
        
        fig = px.line(data)
        st.plotly_chart(fig)
        
    analyze_period(period)
# %%
    def analyze_period2(period):
        scaler = StandardScaler()
        x = pd.DataFrame(df.groupby(by=period)['fl_date'].count())
        x = scaler.fit_transform(x)
        x = x.reshape(-1,)
        scaler2 = StandardScaler()
        y = pd.DataFrame(df.groupby(by=period)['delay_bool'].sum())
        y = scaler2.fit_transform(y)
        y = y.reshape(-1,)
        
        data = pd.DataFrame.from_dict(dict(x=x, y=y))
        
        fig = px.line(data)
        st.plotly_chart(fig)
        
    analyze_period2(period)
        
# %%
    def analyze_period3(period):
        scaler = MinMaxScaler()
        x = pd.DataFrame(df.groupby(by=period)['fl_date'].count())
        x = scaler.fit_transform(x)
        x = x.reshape(-1,)

        scaler2 = MinMaxScaler()
        y = pd.DataFrame((df.groupby(by=period)['delay_bool'].sum() / df.groupby(by=period)['delay_bool'].count())).values
        y = y.reshape(-1,)
            
        data = pd.DataFrame.from_dict(dict(x=x, y=y))
        
        fig = px.line(data)
        st.plotly_chart(fig)
        
    analyze_period3(period)
# %%

    scale = MinMaxScaler() 
    x = pd.DataFrame(pd.cut(df['dep_time'], bins=24).value_counts().sort_index())
    x = scale.fit_transform(x).reshape(-1,)
    x2 = pd.DataFrame(pd.cut(df['dep_time'], bins=24).value_counts().sort_index()).values

    scale2 = MinMaxScaler()
    y = pd.DataFrame(df.groupby(by='hour')['delay_bool'].sum())
    y = scale2.fit_transform(y).reshape(-1,)
    y2 = pd.DataFrame(df.groupby(by='hour')['delay_bool'].sum()).values

    z = y2 / x2
    z = z.reshape(-1,)
    data = pd.DataFrame.from_dict(dict(x=x, y=y, z=z))

    fig = px.line(data)
    st.plotly_chart(fig)
# %%
    st.markdown('''
## Departure Delay Time Analysis: conclusions
1. Arrival delay times
    - For any given time-period, the mean arrival delay is closely related to the number of flights occurring in that time
2. Number of arrival delays
    - For any given time-period, the number of arrival delays is closely related to the number of flights occurring in that time
        - However, when the number of flights is considered, the proportion of flight delays is unrelated to the: 
            - month 
            - week
            - day
            - day of the week
        - The time of day, given in 24 approximate divisions of hours, does seem to have some predictive powers
            - when the number of flights is considered, the proportion of delays does differ among hours
                - The earlier hours (0-3) have high delay times, followed by a steep decline to the (5th) hour and then a steady climb for the rest of the day 
                - An expert on this topic may be able to explain why               
                    ''')
# %%
elif part == 'Analysis of Categorical Variables of Interest':
    st.title('Analysis of Categorical Variables of Interest')
    
    cat = st.radio('Categories',  ('Airlines', 'Airports'))
# %%
    df_cat = df[['mkt_carrier', 'origin', 'dest', 'arr_delay', 'fl_date']].copy(deep=True)
    df_cat['arr_delay'] = df_cat['arr_delay'] > 0
    df_cat['month'] = df_cat.fl_date.dt.month
    if cat == 'Airlines':
    # %%
        y =  df.groupby('mkt_carrier')['arr_delay'].mean()
        x = df.groupby('mkt_carrier')['mkt_carrier'].count()
        fig1 = px.scatter(data_frame=df, x=y.index, y=y.values, size=x, size_max=(60),
                        labels={'x': 'Airline', 'y': 'Mean Arrival Delay', 
                                'size': 'Number of Flights'},
                        title='Arrival Delay by Airline')
        st.plotly_chart(fig1, use_container_width=True)    
    
    
    
    
        x=df_cat.groupby(by=['mkt_carrier'])['fl_date'].count().index
        height=df_cat.groupby(by=['mkt_carrier'])['fl_date'].count().values
        fig = px.bar(x=x, y=height)
        st.plotly_chart(fig)
    # %%
        x = df_cat.groupby(by=['mkt_carrier'])['arr_delay'].sum().index
        height=df_cat.groupby(by=['mkt_carrier'])['arr_delay'].sum().values
        fig = px.bar(x=x, y=height)
        st.plotly_chart(fig)
# %%
    else:
        x=df_cat.groupby(by=['origin'])['fl_date'].count().sort_values(ascending=False)[:15].index  
        height=df_cat.groupby(by=['origin'])['fl_date'].count().sort_values(ascending=False)[:15].values
        fig = px.bar(x=x, y=height)
        st.plotly_chart(fig)

    # %%
        x=df_cat.groupby(by=['dest'])['fl_date'].count().sort_values(ascending=False)[:15].index  
        height=df_cat.groupby(by=['dest'])['fl_date'].count().sort_values(ascending=False)[:15].values
        fig = px.bar(x=x, y=height)
        st.plotly_chart(fig)
# %%
    x = df_cat.groupby(by=['mkt_carrier'])['fl_date'].count().values
    y = df_cat.groupby(by=['mkt_carrier'])['arr_delay'].sum().values
    data = pd.DataFrame.from_dict(dict(x=x, y=y))

    fig = px.scatter(data, x='x', y='y', trendline='ols')
    st.plotly_chart(fig)

# %%
    st.markdown('''
    ## Analysis of Categorical Variables of Interest: conclusions
    Upon initial inspection, the number of delays seemed to be affect by the:
    - airport origin
    - airport dest
    - airline

    However, when considering the flight traffic with respect to each of these categories:
    - Their predictive power disappears                
                ''')

else:
    st.title('Final conclusions')
    
    st.markdown('''
Although the average flight delay is positive the mean flight delay is negative. Thus, most flights are expected to not be delayed, but slightly early. The distribution of delay times is skewed with several few extreme cases, which pushes the average to be higher than the mean. 

The largest predictor of flight delays from this dataset is the amount of flight traffic that occurs.
- the month, week, day, week of day, seem to hold no information about the likelihood of a delay outside of the information they hold about the flight traffic
    - busier times can expect more delays, because they have more flights, but proportionally expect the same frequency of delays as slower times
- the categorical variables. (airline, origin airports, destination airports) hold no predicitve power for flight delays outside of their implicit information for traffic.
    - busier airports can expect more delays, because they have more flights, but proportionally expect the same frequency of delays as smaller airports
- shorter flights seems to have more delays, similarly this seems to be because they are more frequent than longer flights
The hour of the flight seems to have some predictive properties for flight delays that does not completely depend on the traffic.                
                ''')
    if st.button('Celebrate'):
        st.balloons()
    else:
        st.write('You have reached the end. Click the button for a reward.')
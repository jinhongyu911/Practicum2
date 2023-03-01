import pandas as pd
import streamlit as st
import plotly_express as px
import numpy as np

st.header("""
US Vehicle Ad Data Analysis
**Correlations** between different vehicle **attributes**.

***
""")

vehicles = pd.read_csv('C:/Users/Hongyu Jin/python/PracticumProject4/vehicles_us.csv')
vehicles['manufacturer'] = vehicles['model'].str.split().str[0]
vehicles['model_year'] = vehicles['model_year'].fillna(1900).astype(np.int64)

def model_period(year):
    if 1900 <= year <= 1920:
        return '1900-1920'
    if 1920 < year <= 1940:
        return '1921-1940'
    if 1940 < year <= 1960:
        return '1941-1960'
    if 1960 < year <= 1980:
        return '1961-1980'
    if 1980 < year <= 2000:
        return '1981-2000'
    if 2000 < year <= 2020:
        return '2001-2020'

vehicles['model_period'] = vehicles['model_year'].apply(model_period)



st.subheader("""Car Type Distribution by Brand""")
sorted_unique_manufacturer = sorted(vehicles['manufacturer'].unique())
multi_select1 = st.multiselect('Select Manufacturer', sorted_unique_manufacturer, sorted_unique_manufacturer)
df1 = vehicles[vehicles['manufacturer'].isin(multi_select1)]
brand_by_type = pd.pivot_table(df1, values='price', index='manufacturer', columns='type', aggfunc='count')
#brand_by_type.plot(kind='bar', stacked=True, title='Car Type Distribution by Brand', figsize=[10, 5])
st.bar_chart(brand_by_type)



st.subheader("""Car Condition Distribution By Model Year""")
sorted_model_period = sorted(vehicles['model_period'].unique())
multi_select2 = st.multiselect('Select Model Period (up to)', sorted_model_period, sorted_model_period)
df2 = vehicles[vehicles['model_period'].isin(multi_select2)]
mdyr_by_condition = pd.pivot_table(df2, index='model_year', columns='condition', values='price', aggfunc='count')
#mdyr_by_condition.plot(kind='bar', stacked=True, title='Car Condition Distribution By Model Year', figsize=[10, 5])
st.bar_chart(mdyr_by_condition)



st.subheader("""Price Distribution By Brand""")
brand1 = st.selectbox('1st Brand', sorted_unique_manufacturer)
brand2 = st.selectbox('2st Brand', sorted_unique_manufacturer)
brand1_vehicles = vehicles[vehicles['manufacturer'] == brand1]
brand2_vehicles = vehicles[vehicles['manufacturer'] == brand2]

colors = ['#1f77b4', '#c23e3e']
fig1 = px.histogram(brand1_vehicles, x='price', color_discrete_sequence=[colors[0]], opacity=0.8, nbins=20)
fig2 = px.histogram(brand2_vehicles, x='price', color_discrete_sequence=[colors[1]], opacity=0.5, nbins=20)
fig_combined = fig1.add_trace(fig2.data[0])
#fig_combined.update_traces(name=[brand1, brand2])
fig_combined.update_layout(barmode='overlay', xaxis_title='Price', yaxis_title='Count',
                            title='Price Distribution by Brand')
st.plotly_chart(fig_combined)



st.subheader("""Car Price vs Model Year""")
sorted_model_period = sorted(vehicles['model_period'].unique())
multi_select2 = st.multiselect('Select Model Years (up to)', sorted_model_period, sorted_model_period)
df3 = vehicles[vehicles['model_period'].isin(multi_select2)]
#vehicles.plot(kind='scatter', y='price', x='model_year', title='Car Price vs Model Year', figsize=[10, 5])
fig = px.scatter(df3, x="model_year", y="price", color='condition')
st.plotly_chart(fig)

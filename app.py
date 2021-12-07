import streamlit as st
import pandas as pd
import numpy as np

st.title("HK Properties")


df = pd.read_csv('./rental.csv', index_col=0)

district_list = np.append(['Show All'], df['District'].unique())
usage_list = np.append(['Show All'], df['District'].unique())

district = st.sidebar.selectbox("District", district_list, index=0)
usage = st.sidebar.selectbox("Usage", usage_list, index=0)

min_size = st.sidebar.slider("Minimum Size", step=10, min_value=int(np.min(df['Gross Area (ft²)'])), max_value=int(np.max(df['Gross Area (ft²)'])))
max_size = st.sidebar.slider("Maximum Size", min_value=int(min_size), max_value=int(np.max(df['Gross Area (ft²)'])), step=10, value=int(np.max(df['Gross Area (ft²)'])))

min_rent = st.sidebar.slider("Minimum Rent", min_value=int(df['Rental'].min()), max_value=int(df['Rental'].max()), step=10)
max_rent = st.sidebar.slider("Maximum Rent", min_value=int(min_rent), max_value=int(df['Rental'].max()), step=10, value=int(df['Rental'].max()))

df2 = df.copy()
df2 = df2.dropna(axis=0)

if usage == 'Show All':
    pass
else:
    df2 = df2[df2['Usage'] == usage]

if district == 'Show All':
    pass
else:
    df2 = df2[df2['District'] == district]

df2 = df2[(df2['Gross Area (ft²)'] <= max_size) & (df2['Gross Area (ft²)'] >= min_size)]
df2 = df2[(df2['Rental'] <= max_rent) & (df2['Rental'] >= min_rent)]
st.dataframe(df2)

df3 = df.copy()
df3 = df3.dropna(axis=0)
avg_price_df = round(np.mean(df['Rental per ft²']), 2)
df3_res = df3[df3['Usage'] == 'Residential']
df3_comm = df3[df3['Usage'] == 'Commercial Shop']
df3_off = df3[df3['Usage'] == 'Office']
st.write(f"Average rent per square foot in above selection: ${avg_price_df}/sqft")
st.write('----------------------')
st.write(f"Average rent per square foot for HK Residential Properties: ${round(np.mean(df3_res['Rental per ft²']), 2)}/sqft")
st.write(f"Average rent per square foot for HK Commercial Properties: ${round(np.mean(df3_comm['Rental per ft²']), 2)}/sqft")
st.write(f"Average rent per square foot for HK Office Properties: ${round(np.mean(df3_off['Rental per ft²']), 2)}/sqft")

st.write('----------------------')
for d in df3['District'].unique():
    df4 = df3[df3['District'] == d]['Rental per ft²']
    st.write(f"Average Property Price in {d} is: ${round(np.mean(df4), 2)}/sqft")

df5 = df3.copy()

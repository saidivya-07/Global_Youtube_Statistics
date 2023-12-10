import streamlit as st
import pandas as pd

st.markdown('Youtube Statistics')

df= pd.read_csv('M_Global_YouTube_Statistics.csv')
st.dataframe(df)


import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import calplot
import numpy as np

st.set_page_config(page_title="Visualizar horas", page_icon="🕒", layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Controle de horas")

df = load_main_dataframe("Horas por dia")

df["Dia"] = pd.to_datetime(df["Dia"])
df["period"] = df["Dia"].dt.to_period('M')

filter = st.selectbox("Selecione o mês", df["period"].unique())

filtered_df = df.loc[df["period"] == filter]

st.dataframe(filtered_df)

bar_chart = px.bar(filtered_df, x='Dia', y='Horas trabalhadas')

st.plotly_chart(bar_chart, use_container_width=True)

all_days = pd.date_range('1/1/2019', periods=360, freq='D')
days = np.random.choice(all_days, 500)
events = pd.Series(np.random.randn(len(days)), index=days)
teste = calplot.calplot(events, edgecolor=None, cmap='YlGn')

st.plotly_chart(teste, use_container_width=True)

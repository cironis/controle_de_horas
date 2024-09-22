
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Visualizar horas", page_icon="🕒", layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Controle de horas")

# Carregando df das horas trabalhadas
df_horas = load_main_dataframe("Horas por dia")

df_horas["Dia"] = pd.to_datetime(df_horas["Dia"])
df_horas["ano"] = df_horas["Dia"].dt.year

df_horas["dia_da_semana"] = df_horas["Dia"].dt.day_name()
df_horas["period"] = df_horas["Dia"].dt.to_period('M')

# Criando df para o Heatmap
dias_no_ano = pd.date_range(start=f'{df_horas["ano"].min()}-01-01', end=f'{df_horas["ano"].max()}-12-31', freq='D')

heatmap_df = pd.DataFrame({
    'Data': dias_no_ano,
    'Horas trabalhadas': np.zeros(len(dias_no_ano))
})


filter = st.selectbox("Selecione o mês", df["period"].unique())

filtered_df = df.loc[df["period"] == filter]

st.dataframe(filtered_df)

bar_chart = px.bar(filtered_df, x='Dia', y='Horas trabalhadas')

st.plotly_chart(bar_chart, use_container_width=True)

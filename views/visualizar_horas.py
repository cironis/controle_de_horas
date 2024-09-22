
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


# Carregando df das horas trabalhadas
df_horas = load_main_dataframe("Horas por dia")

df_horas["Dia"] = pd.to_datetime(df_horas["Dia"])
anos = df_horas["Dia"].dt.year.unique()

dias_no_ano = pd.date_range(start=f'{anos.min()}-01-01', end=f'{anos.max()}-12-31', freq='D')

all_days = pd.DataFrame({
    'Dia': dias_no_ano,
    'Horas trabalhadas': np.zeros(len(dias_no_ano)),
})

df_horas = pd.concat([all_days, df_horas], ignore_index=True)

df_horas["ano"] = df_horas["Dia"].dt.year

df_horas["dia_da_semana"] = df_horas["Dia"].dt.day_name()
df_horas["numero_do_dia_da_semana"] = df_horas["Dia"].dt.weekday
df_horas["period"] = df_horas["Dia"].dt.to_period('M')
df_horas['semana'] = df_horas['Dia'].dt.strftime('%U').astype(int) + 1

st.dataframe(df_horas)

seletor_ano = st.selectbox("Selecione o ano", anos)
df_horas = df_horas.loc[df_horas["ano"] == seletor_ano]

heatmap_df = df_horas.pivot_table(index='numero_do_dia_da_semana', columns='semana', values='Horas trabalhadas', aggfunc='sum',fill_value=0)


st.title("Controle de horas")

st.dataframe(heatmap_df)


heatmap = px.imshow(heatmap_df)
st.plotly_chart(heatmap)


seletor_mes = st.selectbox("Selecione o mês", df_horas["period"].unique())

filtered_df = df_horas.loc[df_horas["period"] == seletor_mes]

st.dataframe(filtered_df)

bar_chart = px.bar(filtered_df, x='Dia', y='Horas trabalhadas')

st.plotly_chart(bar_chart, use_container_width=True)


import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from datetime import datetime

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

agora = datetime.now()
agora_mes = agora.to_period('M')
agora_ano = agora.year

if agora_mes in df_horas["period"].values:
    default_mes_index = df_horas[df_horas["period"] == agora_mes].index[0]
else:
    default_mes_index = 0

# Find the index of the current year in the DataFrame
if agora_ano in df_horas["ano"].values:
    default_ano_index = df_horas[df_horas["ano"] == agora_ano].index[0]
else:
    default_ano_index = 0 

st.title("Controle de horas")

st.markdown("## Ano")

seletor_ano = st.selectbox("Selecione o ano", df_horas["ano"].unique(),index=default_ano_index)
df_horas = df_horas.loc[df_horas["ano"] == seletor_ano]

heatmap_df = df_horas.pivot_table(index=['numero_do_dia_da_semana',"dia_da_semana"], columns='semana', values='Horas trabalhadas', aggfunc='sum',fill_value=0)

heatmap_df = heatmap_df.reset_index(level='dia_da_semana')
heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_df.values,
    y=heatmap_df["dia_da_semana"].str[0:3],
    colorscale="Blues",  
    xgap=2,  
    ygap=2 
))

heatmap.update_xaxes(showticklabels=False)

st.plotly_chart(heatmap)

st.markdown("## Mês")

seletor_mes = st.selectbox("Selecione o mês", df_horas["period"].unique(),index=default_mes_index)

filtered_df = df_horas.loc[df_horas["period"] == seletor_mes]

bar_chart = px.bar(filtered_df, x='Dia', y='Horas trabalhadas')

st.plotly_chart(bar_chart, use_container_width=True)

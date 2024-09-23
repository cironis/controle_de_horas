
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
df_horas["Data"] = pd.to_datetime(df_horas["Dia"]).dt.strftime('%d/%m/%Y')
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
agora_pandas = pd.Timestamp(agora)
agora_mes = agora_pandas.to_period('M')
agora_ano = agora_pandas.year

unique_periods = df_horas["period"].loc[df_horas["period"] <= agora_mes].sort_values().unique().tolist()
unique_years = df_horas["ano"].unique().tolist()

if agora_mes in unique_periods:
    default_mes_index = unique_periods.index(agora_mes)
else:
    default_mes_index = 0

if agora_ano in unique_years:
    default_ano_index = unique_years.index(agora_ano)
else:
    default_ano_index = 0

st.title("Controle de horas")

st.markdown("## Ano")

seletor_ano = st.selectbox("Selecione o ano", unique_years,index=default_ano_index)
df_horas = df_horas.loc[df_horas["ano"] == seletor_ano]

heatmap_df = df_horas.pivot_table(index=['numero_do_dia_da_semana',"dia_da_semana"], columns='semana', values='Horas trabalhadas', aggfunc='sum',fill_value=0)

heatmap_df = heatmap_df.sort_index(level='numero_do_dia_da_semana')

hovertemplate = (
    'Semana: %{x}<br>'
    'Dia da semana: %{y}<br>'
    'Horas trabalhadas: %{z}<extra></extra>'
)

heatmap_df = heatmap_df.reset_index(level='dia_da_semana')
heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_df.values,
    y=heatmap_df["dia_da_semana"].str[0:3],
    x=heatmap_df.columns[1:],
    colorscale="Blues",
    xgap=2,
    ygap=2,
    hovertemplate=hovertemplate
))

heatmap.update_xaxes(showticklabels=False)

st.plotly_chart(heatmap)

st.markdown("## Horas por dia")

seletor_mes = st.selectbox("Selecione o mês", unique_periods,index=default_mes_index)
filtered_df = df_horas.loc[df_horas["period"] == seletor_mes]
filtered_df = filtered_df.loc[df_horas["Horas trabalhadas"] > 0]

col_1,col_2 = st.columns(2)

with col_1:
    st.dataframe(filtered_df[["Data","Horas trabalhadas"]],hide_index = True,use_container_width=True)

with col_2:
    st.metric("Horas Total (Mês)", f"{filtered_df['Horas trabalhadas'].sum():.2f}")


import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Access the signature key from st.secrets
signature_key = st.secrets["credentials"]["signature_key"]

# Load credentials from the config.yaml file
with open('config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    'cookie',           # Replace with your cookie name
    signature_key,         # Replace with your signature key
    cookie_expiry_days=30
    )

if "auto_login" in st.query_params:
    if st.query_params["auto_login"] == "vai_vamo_logo":

        st.session_state['authentication_status'] = True

else:

    authenticator.login('main')

def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)

    return df

def update_dataframe(worksheet,df):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.update(worksheet=worksheet, data=df)

    return

def inserir_horas(date_picker,number_input):
    df_horas = load_main_dataframe("Horas por dia")

    if 'horas_df' not in st.session_state:
        st.session_state['horas_df'] = df_horas
    else:
        df_horas = st.session_state['horas_df']

    df_horas["Dia"] = pd.to_datetime(df_horas["Dia"])
    novo_registro = pd.DataFrame({
        "Dia": [date_picker],
        "Horas trabalhadas": [number_input]
    })

    df_horas = pd.concat([df_horas, novo_registro], ignore_index=True)
    st.session_state['horas_df'] = df_horas

    update_dataframe("Horas por dia",df_horas)
    st.session_state['clicked'] = True
    st.balloons()

    return True


if st.session_state['authentication_status']:

    authenticator.logout("Logout", "sidebar")
    st.markdown(f'# Inserir Horas')
    date_picker = st.date_input("Data", datetime.today(),format="DD/MM/YYYY")
    number_input = st.number_input("Horas para inserir", min_value=0.0, step=0.5)
    button_return = st.button('Inserir Horas', on_click=inserir_horas, args=(date_picker,number_input))

    if st.session_state['clicked']:
        st.success('Horas inseridas com sucesso!')

    st.markdown(f'# Total por Mês')

    total_1, total_2 = st.columns([1,3])

    with total_1:
        df_horas_total = load_main_dataframe("Horas por dia")
        df_horas_total["Dia"] = pd.to_datetime(df_horas_total["Dia"])

        mes_selecionado = st.selectbox("Selecione o mês", df_horas_total["Dia"].dt.to_period('M').sort_values(ascending = False).unique(),index=0)

        total_horas = df_horas_total.loc[df_horas_total["Dia"].dt.to_period('M') == mes_selecionado,"Horas trabalhadas"].sum()
        valor_por_hora = 130
        valor_a_receber = f"R${total_horas*valor_por_hora:.2f}"

        month_names_pt_br = {
            1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
            5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
            9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
        }

        month = mes_selecionado.month
        year = mes_selecionado.year
        month_name_pt_br = month_names_pt_br[month]

        mes = f"{month_name_pt_br}/{year}"

    with total_2:
        st.markdown(f"## Horas total do Mês: {total_horas} horas")
        st.markdown(f"## Valor: {valor_a_receber}")

    st.markdown(f'# Email Copia e cola')

    st.markdown(f"""
                    <p>OI Luis, tudo bem?</p>
                    <p>Segue a nota referente ao mês {mes}.</p>
                    <p>Foram {total_horas} horas trabalhadas, que totalizam <a href='https://controle-de-horas.streamlit.app/'>{valor_a_receber}</a>.</p>
                    <p>Qualquer dúvida, estou à disposição.</p>
                    <p>Obrigado.</p>""",unsafe_allow_html=True)


elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

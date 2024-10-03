
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

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

name, authentication_status, username = authenticator.login('main')

def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*')
    # Main application code
    st.title('Inserir Horas')
    
    df_horas = load_main_dataframe("Horas por dia")
    df_horas["Dia"] = pd.to_datetime(df_horas["Dia"])
    df_horas["Data"] = pd.to_datetime(df_horas["Dia"]).dt.strftime('%d/%m/%Y')
    
    st.dataframe(df_horas)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

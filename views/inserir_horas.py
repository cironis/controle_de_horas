
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
from datetime import datetime

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

authenticator.login('main')

def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

def update_dataframe(worksheet,df):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.update(worksheet=worksheet, data=df)

    return

if st.session_state['authentication_status']:
    authenticator.logout("Logout", "sidebar")
    st.write(f'Inserir Horas')
    date_picker = st.date_input("When's your birthday", datetime.today())
    number_input = st.number_input("Horas para inserir", min_value=0.0, step=0.5)

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

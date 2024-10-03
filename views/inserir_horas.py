
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

authenticator.login('main')

def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

if st.session_state['authentication_status']:
    authenticator.logout("Logout", "sidebar")
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')


import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from aux.boargamegeek_api import query_boardgamegeek, get_game_info
from aux.aggrid_builder import create_grid
import pandas as pd

# Access the signature key from st.secrets
signature_key = st.secrets["credentials"]["signature_key"]

# Load credentials from the config.yaml file
with open('config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    'the_cookie',           # Replace with your cookie name
    signature_key,         # Replace with your signature key
    cookie_expiry_days=30
)

# Login widget
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f'Welcome *{name}*')
    # Main application code
    st.title('Cadastrar Jogos')

    # Create a search box
    search_query = st.text_input("Enter your search query", "")

    # Create a button to trigger the search
    search_button = st.button("Search")

    # Trigger the search function when the button is clicked or Enter is pressed
    if search_button or search_query:
        if search_query:
            results_df = query_boardgamegeek(search_query)
            if not results_df.empty:
                grid = create_grid(results_df,True)
                st.write(grid['selected_rows'])
            else:
                st.warning("No results found.")

        else:
            st.error("Please enter a search query.")


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

import streamlit as st

# --- PAGE SETUP ---
visualizar_horas = st.Page(
    "views/visualizar_horas.py",
    title="Consultoria - Pró-Corpo",
    icon=":material/overview:",
)

inserir_horas = st.Page(
    "views/inserir_horas.py",
    title="Área Logada",
    icon=":material/overview:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Visualização": [visualizar_horas],
        "Área logada": [inserir_horas]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")

# --- RUN NAVIGATION ---
pg.run()

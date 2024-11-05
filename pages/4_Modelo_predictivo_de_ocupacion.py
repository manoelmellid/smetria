import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo predictivo de ocupación")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

# Crear un sistema simple de login manual
def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("Inicio de sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            if username == 'usuario' and password == 'password123':
                st.session_state.logged_in = True
                st.session_state.role = 'user'
                st.success("Bienvenido, Usuario Normal")
            elif username == 'admin' and password == 'adminpassword':
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.success("Bienvenido, Personal")
            else:
                st.error("Usuario o contraseña incorrectos")
    
    else:
        if st.session_state.role == 'admin':
            st.write("Bienvenido al área de personal.")
            st.write("Datos privados de flujo...")
        else:
            st.write("Bienvenido, usuario normal.")
            st.write("Información pública...")

login()


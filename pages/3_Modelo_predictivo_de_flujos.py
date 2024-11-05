import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Modelo predictivo de flujos")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
    
    # Si no está logueado, el sistema solo permitirá el login si el usuario es admin
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            # Solo se permite login para el admin
            if username == 'admin' and password == 'adminpassword':
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.success("Bienvenido, Administrador")
            else:
                st.session_state.logged_in = False
    
    # Si está logueado, muestra las vistas según el rol
    if st.session_state.logged_in == True:
        st.write("Bienvenido al área de personal.")
        st.write("Datos privados de flujo...")
    else:
        st.write("Bienvenido, usuario normal.")
        st.write("Información pública...")

login()

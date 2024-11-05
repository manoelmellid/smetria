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
import streamlit as st

def login():
    # Inicializamos el estado de sesión si aún no se ha hecho
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None

    # Si no está logueado, verificamos si es admin
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar sesión"):
            # Solo el admin necesita hacer login
            if username == 'admin' and password == 'adminpassword':
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.success("Bienvenido, Administrador")
            else:
                # Los demás usuarios son considerados 'user' y no necesitan login
                st.session_state.logged_in = True
                st.session_state.role = 'user'
                st.success("Bienvenido, Usuario Normal")
    
    # Una vez logueado, mostramos el contenido según el rol
    if st.session_state.logged_in:
        if st.session_state.role == 'admin':
            st.write("Bienvenido al área de personal.")
            st.write("Datos privados de flujo...")
        elif st.session_state.role == 'user':
            st.write("Bienvenido, usuario normal.")
            st.write("Información pública...")
        else:
            st.error("Rol no reconocido")

login()


import streamlit as st

def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
    
    # Si no está logueado, el sistema solo permitirá el login si el usuario es admin
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        # Obtener las credenciales de st.secrets
        admin_username = st.secrets["admin_username"]
        admin_password = st.secrets["admin_password"]
        
        if st.button("Iniciar sesión"):
            # Solo se permite login para el admin
            if username == admin_username and password == admin_password:
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.success("Bienvenido, Administrador")
            else:
                st.session_state.logged_in = False
    return st.session_state.logged_in

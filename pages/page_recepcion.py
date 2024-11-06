import streamlit as st
from utils import general as gen, github as git

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    df = git.leer_archivo_github()
    if not df.empty:
        st.write(df)
    else:
        st.write("El archivo no se pudo cargar o está vacío.")

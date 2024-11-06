import streamlit as st
from utils import general as gen, github as git

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    # Mostrar la tabla en Streamlit
    st.table(git.leer_archivo_github())

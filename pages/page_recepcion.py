import streamlit as st
from utils import general as gen, github as git

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    # Cargar los datos filtrados
    df = git.cargar_datos(columnas_necesarias=['id', 'fecha', 'nombre', 'email', 'ubicacion', 'tipo_incidencia', 'comentario'])
    # Mostrar la tabla en Streamlit
    st.dataframe(df)

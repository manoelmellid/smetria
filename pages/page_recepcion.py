import streamlit as st
from utils import general as gen

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
def visualizar_archivo():
    # Leer el archivo contactos.csv y cargarlo en una lista
    try:
        with open('contactos.csv', mode='r') as file:
            reader = csv.reader(file)
            datos = list(reader)
            if datos:
                # Crear un dataframe a partir de los datos y mostrarlo
                st.write("### Incidencias Registradas")
                st.dataframe(datos)  # Puedes usar st.table(datos) si no quieres la funcionalidad interactiva
            else:
                st.write("No hay datos disponibles.")
    except FileNotFoundError:
        st.write("El archivo contactos.csv no existe aún.")

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    visualizar_archivo()
else:

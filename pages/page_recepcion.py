import streamlit as st
from utils import general as gen, github as git

st.header("Sistema de recepción de incidencias")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
    st.write("Bienvenido al área de personal.")
    # Cargar los datos filtrados
    df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'nombre', 'email', 'latitud', 'longitud', 'tipo_incidencia', 'comentario'])
    # Mostrar la tabla en Streamlit
    st.write(df)
    id_input = st.text_input("Ingrese el ID de la incidencia a solucionar:")
    # Botón para cambiar el estado
    if st.button("Marcar como Solucionado"):
        if id_input:
            if id_input in df['id'].values:
                git.actualizar_estado(id_input)
            else:
                st.error(f"No se encontró una incidencia con el ID {id_input}.")
        else:
            st.error("Por favor, ingrese un ID para la incidencia.")

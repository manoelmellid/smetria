import streamlit as st
from utils import general as gen, github as git

st.header("Sistema de recepción de incidencias")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    
    # Cargar los datos filtrados
    df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'nombre', 'email', 'latitud', 'longitud', 'tipo_incidencia', 'comentario'])

    # Mostrar la tabla en Streamlit
    st.dataframe(df)
    
    # Añadir un campo para ingresar un ID
    id_input = st.text_input("Ingrese el ID de la incidencia a solucionar:")
    
    # Botón para cambiar el estado
    if st.button("Marcar como Solucionado"):
        # Verificar si el ID ingresado existe en el DataFrame
        if id_input:
            if id_input.isdigit():  # Verificar que el ID es un número
                id_input = int(id_input)
                if id_input in df['id'].values:
                    # Actualizar el estado de la incidencia
                    df.loc[df['id'] == id_input, 'estado'] = 'Solucionado'
                    st.success(f"La incidencia con ID {id_input} ha sido marcada como 'Solucionado'.")
                else:
                    st.error(f"No se encontró una incidencia con el ID {id_input}.")
            else:
                st.error("Por favor, ingrese un ID válido (número).")
        else:
            st.error("Por favor, ingrese un ID para la incidencia.")

    # Mostrar la tabla actualizada
    st.dataframe(df)

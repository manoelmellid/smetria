import streamlit as st
from utils import general as gen, github as git

st.header("Sistema de recepción de incidencias")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
    st.success("Bienvenido al área de Recepción del Sistema de Notificacion de Incidencias.")
    # Cargar los datos filtrados
    df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'latitud', 'longitud', 'tipo_incidencia', 'tipo_alerta', 'comentario'])
    # Mostrar la tabla en Streamlit
    st.write(df)
    
    tipo_opc = st.selectbox('Selecciona la opción:', ['Cambio de estado', 'Cambio del nivel de alerta', 'Cambio de tipo'])
    
    if tipo_opc == 'Cambio de estado':
        id_input = st.text_input("Ingrese el ID de la incidencia a solucionar:")
        cambio_estado = st.selectbox('Cambio a realizar:', ['Solucionado', 'Activo', 'Inactivo'])
        if st.button("Marcar como Solucionado"):
            if id_input:
                if id_input in df['id'].values:
                    git.actualizar(id_input, 'estado', cambio_estado)
                else:
                    st.error(f"No se encontró una incidencia con el ID {id_input}.")
            else:
                st.error("Por favor, ingrese un ID para la incidencia.")
    elif tipo_opc == 'Cambio del nivel de alerta':
        st.warning("Gracias por colaborar")

import streamlit as st
import pandas as pd
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
    
    tipo_opc = st.selectbox('Selecciona la opción:', ['Cambio de estado', 'Cambio del nivel de alerta', 'Cambio de tipo de incidencia'])
    
    if tipo_opc == 'Cambio de estado':
        id_input = st.text_input("Ingrese el ID de la incidencia a modificar:")
        cambio_estado = st.selectbox('Cambio a realizar:', ['Solucionado', 'Activo', 'Inactivo'])
        if st.button("Cambiar estado"):
            if id_input:
                if id_input in df['id'].values:
                    #st.warning("Esta herramienta es funcional pero está descactivada temporalmente")
                    st.info("Cambio realizado")
                    git.actualizar(id_input, 'estado', cambio_estado)
                else:
                    st.error(f"No se encontró una incidencia con el ID {id_input}.")
            else:
                st.error("Por favor, ingrese un ID para la incidencia.")
                
    elif tipo_opc == 'Cambio del nivel de alerta':
        id_input = st.text_input("Ingrese el ID de la incidencia a modificar:")
        cambio_alerta = st.selectbox('Cambio a realizar:', ['Alta', 'Media', 'Baja'])
        if st.button("Cambiar nivel de alerta"):
            if id_input:
                if id_input in df['id'].values:
                    st.warning("Esta herramienta es funcional pero está descactivada temporalmente")
                    #git.actualizar(id_input, 'tipo_alerta', cambio_alerta)
                else:
                    st.error(f"No se encontró una incidencia con el ID {id_input}.")
            else:
                st.error("Por favor, ingrese un ID para la incidencia.")
                
    elif tipo_opc == 'Cambio de tipo de incidencia':
        opciones_df = pd.read_csv('datasets/opciones_incidencias.csv')
        id_input = st.text_input("Ingrese el ID de la incidencia a modificar:")
        cambio_tipo = st.selectbox('Cambio a realizar:', opciones_df['tipo'].tolist())
        cambio_alerta = opciones_df.loc[opciones_df['tipo'] == cambio_tipo, 'alerta'].iloc[0]
        if st.button("Cambiar tipo de incidencia"):
            if id_input:
                if id_input in df['id'].values:
                    st.warning("Esta herramienta es funcional pero está descactivada temporalmente para evitar cambios involuntarios")
                    #git.actualizar(id_input, 'tipo', cambio_tipo)
                    #git.actualizar(id_input, 'tipo_alerta', cambio_alerta)
                else:
                    st.error(f"No se encontró una incidencia con el ID {id_input}.")
            else:
                st.error("Por favor, ingrese un ID para la incidencia.")

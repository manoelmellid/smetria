import streamlit as st
import csv
import pandas as pd
from utils import general as gen, github as git

st.header("Sistema de notificación de incidencias")

opciones_df = pd.read_csv('opciones_incidencias.csv')

# Campos del formulario
nombre = st.text_input("Nombre y apellidos")
telefono = st.text_input("Teléfono")

if telefono:
    if not gen.validar_telefono(telefono):
        st.error("Por favor, ingrese un número de teléfono válido.")
        
email = st.text_input("Correo electrónico")
input_text = st.text_input("Indique el Km del Camino dónde se encuentra")
opciones = ['Crecida de río', 'Incendio', 'Desprendimiento de tierra', 'Tramo colapsado/cerrado', 'Mobiliario deteriorado', 'Accidente en el camino', 'Animales sueltos', 'Fuente sin agua']
tipo_opc = st.selectbox('Selecciona el tipo de incidencia:', opciones_df['tipo'].tolist())
alerta_opc = opciones_df.loc[opciones_df['tipo'] == tipo_opc, 'alerta'].iloc[0]
mensaje = st.text_area("Añada más detalles si lo considera necesario:")

if st.button("Enviar"):
    if nombre and email and telefono and input_text:
        # Llamar a la función para guardar en GitHub
        git.guardar_respuesta_en_csv(
            nombre=nombre,
            telefono=telefono,
            email=email,
            input_text=input_text,
            tipo_opc=tipo_opc,
            mensaje=mensaje,
            alerta_opc=alerta_opc
        )
        st.success("Notificación enviada con éxito.")
    else:
        st.error("Por favor, cubra los campos obligatorios.")
    



import streamlit as st
import csv
from utils import general as gen, github as git

st.header("Sistema de notificación de incidencias")
st.header("SINICAS")

# Campos del formulario
nombre = st.text_input("Nombre y apellidos")
email = st.text_input("Correo electrónico")
input_text = st.text_input("Indique el Km del Camino dónde se encuentra")
opciones = ['Crecida de río', 'Incendio', 'Desprendimiento de tierra', 'Tramo colapsado/cerrado', 'Mobiliario deteriorado', 'Accidente en el camino', 'Animales sueltos', 'Fuente sin agua']
tipo_opc = st.selectbox('Selecciona una opción:', opciones)
mensaje = st.text_area("Añada más detalles si lo considera necesario:")

if st.button("Enviar"):
    if nombre and email:
        # Llamar a la función para guardar en GitHub
        git.guardar_respuesta_en_csv(
            nombre=nombre,
            email=email,
            input_text=input_text,
            tipo_opc=tipo_opc,
            mensaje=mensaje,
        )
        st.success("Notificación enviada con éxito y guardada en GitHub.")
    else:
        st.error("Por favor, cubra los campos obligatorios.")
    



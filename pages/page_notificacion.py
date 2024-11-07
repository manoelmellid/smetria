import streamlit as st
import csv
from utils import general as gen, github as git

st.header("Sistema de notificación de incidencias")

# Campos del formulario
nombre = st.text_input("Nombre")
email = st.text_input("Correo electrónico")
opciones = ['Crecida de río', 'Incendio', 'Desprendimiento de tierra', 'Tramo colapsado/cerrado', 'Mobiliario deteriorado', 'Accidente en el camino', 'Animales sueltos', 'Fuente sin agua']
tipo = st.selectbox('Selecciona una opción:', opciones)
mensaje = st.text_area("Añada más detalles si lo considera necesario:")

if st.button("Enviar"):
    if nombre and email and mensaje:
        st.success("¡Mensaje guardado con éxito!")
    else:
        st.error("Por favor, llena todos los campos.")
    



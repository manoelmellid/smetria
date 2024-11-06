import streamlit as st
import csv
from utils import general as gen, github as git

st.header("Sistema de notificación de incidencias")

# Campos del formulario
nombre = st.text_input("Nombre")
email = st.text_input("Correo electrónico")
mensaje = st.text_area("Mensaje")
# Usar la función cuando el formulario se envíe

if st.button("Enviar"):
    if nombre and email and mensaje:
        git.guardar_en_archivo(nombre, email, mensaje):
        st.success("¡Mensaje guardado con éxito!")
    else:
        st.error("Por favor, llena todos los campos.")
    



import streamlit as st
from utils import general as gen

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")
  
import re

# Función para validar el número de teléfono
def validar_telefono(telefono):
    # Expresión regular para un formato de número de teléfono (ej. +34 612 345 678)
    patron = r"^\+?[0-9]{1,3}?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}$"
    if re.match(patron, telefono):
        return True
    return False

# Crear un campo de texto para el teléfono
telefono = st.text_input("Teléfono")

# Validación
if telefono:
    if not validar_telefono(telefono):
        st.error("Por favor, ingrese un número de teléfono válido.")
    else:
        st.success("Número de teléfono válido.")

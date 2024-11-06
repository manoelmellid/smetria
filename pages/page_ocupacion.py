import streamlit as st
import pandas as pd
import numpy as np
from utils import github as git

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

# Ejemplo de uso
nombre = 'Juan Pérez'
email = 'juan.perez@email.com'
mensaje = 'Este es un mensaje de prueba.'
git.guardar_en_archivo(nombre, email, mensaje)

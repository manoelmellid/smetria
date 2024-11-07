import streamlit as st
import pandas as pd
from utils import github as git

# Cargar los datos especificando solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'latitud', 'longitud', 'tipo_incidencia'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo']

# Mostrar el mapa con los puntos de las ubicaciones activas
# Seleccionar solo las columnas 'latitud' y 'longitud' para el mapa
st.map(df_activo[['latitud', 'longitud']])

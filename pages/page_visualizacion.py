import streamlit as st
import pandas as pd
from utils import github as git

# Cargar los datos con solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'latitud', 'longitud', 'tipo_incidencia'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo']

# Renombrar las columnas para que Streamlit las reconozca como coordenadas
df_activo = df_activo.rename(columns={'latitud': 'latitude', 'longitud': 'longitude'})

# Mostrar el mapa con los puntos de las ubicaciones activas
st.map(df_activo[['latitude', 'longitude']])

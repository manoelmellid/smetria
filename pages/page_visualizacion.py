import streamlit as st
import pandas as pd
from utils import github as git

# Cargar los datos con solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'ubicacion', 'tipo_incidencia'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo'].copy()

# Validar que todas las ubicaciones tienen el formato correcto [latitud, longitud]
df_activo = df_activo[df_activo['ubicacion'].apply(lambda x: isinstance(x, list) and len(x) == 2)]

# Extraer latitud y longitud de la columna 'ubicacion'
df_activo[['latitud', 'longitud']] = pd.DataFrame(df_activo['ubicacion'].tolist(), index=df_activo.index)

# Mostrar el mapa con los puntos de las ubicaciones activas
st.map(df_activo[['latitud', 'longitud']])

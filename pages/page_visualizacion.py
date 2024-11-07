import streamlit as st
from utils import github as git

df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'ubicacion', 'tipo_incidencia'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo']

# Extraer latitud y longitud de la columna 'ubicacion'
# Creamos dos nuevas columnas 'latitud' y 'longitud' a partir de 'ubicacion'
df_activo[['latitud', 'longitud']] = pd.DataFrame(df_activo['ubicacion'].tolist(), index=df_activo.index)

# Mostrar el mapa con los puntos de las ubicaciones activas
st.map(df_activo[['latitud', 'longitud']])

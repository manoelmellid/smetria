import streamlit as st
import pandas as pd
import pydeck as pdk
from utils import github as git

st.header("Mapa de visualización de incidencias")
# ---------------------------------------------------------------------------------

# Cargar los datos con solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'latitud', 'longitud', 'tipo_incidencia'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo']

# Renombrar las columnas para que Streamlit las reconozca como coordenadas
df_activo = df_activo.rename(columns={'latitud': 'latitude', 'longitud': 'longitude'})

# Mostrar el mapa con los puntos de las ubicaciones activas
#st.map(df_activo[['latitude', 'longitude']])

layer = pdk.Layer(
    'ScatterplotLayer',
    df_activo,
    get_position='[longitude, latitude]',
    get_radius=50,  # Tamaño del punto
    get_fill_color=[255, 0, 0, 160],  # Color del punto (rojo)
    pickable=True,
    auto_highlight=True
)

# Agregar etiquetas de texto (Tipo) sobre los puntos
tooltip = {
    "html": "<b>Tipo:</b> {Tipo}",  # Mostrar el tipo de cada ubicación
    "style": {"color": "white", "backgroundColor": "rgba(0,0,0,0.7)", "padding": "5px"}
}

# Crear la vista del mapa
view_state = pdk.ViewState(
    latitude=df_activo['latitude'].mean(),
    longitude=df_activo['longitude'].mean(),
    zoom=12
)

# Renderizar el mapa con pydeck
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(deck)

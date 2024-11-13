import streamlit as st
import pandas as pd
import pydeck as pdk
from utils import github as git

st.header("Mapa de visualización de incidencias")
st.error("Esta sección de SMETRIA está en desarrollo todavía")
# ---------------------------------------------------------------------------------
# Cargar los datos con solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'latitud', 'longitud', 'tipo_incidencia', 'tipo_alerta'])

# Filtrar el DataFrame para que solo contenga filas con 'estado' == 'Activo'
df_activo = df[df['estado'] == 'Activo']

# Asegurarse de que las coordenadas sean de tipo float
df_activo['latitude'] = pd.to_numeric(df_activo['latitud'], errors='coerce')
df_activo['longitude'] = pd.to_numeric(df_activo['longitud'], errors='coerce')

# Crea la capa para el mapa
layer = pdk.Layer(
    'ScatterplotLayer',
    df_activo,
    get_position='[longitude, latitude]',
    get_radius=200,  # Tamaño del punto
    get_fill_color=[255, 0, 0, 160],  # Color del punto (rojo)
    pickable=True,
    auto_highlight=True
)

# Agregar etiquetas de texto (Tipo de incidencia) sobre los puntos
tooltip = {
    "html": "<b>PELIGRO - </b> {tipo_incidencia}",  # Mostrar el tipo de cada ubicación
    "style": {"color": "white", "backgroundColor": "rgba(0,0,0,0.7)", "padding": "5px"}
}

# Crear la vista del mapa
view_state = pdk.ViewState(
    latitude=df_activo['latitude'].mean(),
    longitude=df_activo['longitude'].mean(),
    zoom=12,  # Puedes ajustar el zoom según el alcance de las coordenadas
    pitch=0,  # Sin inclinación
    bearing=0  # Sin rotación
)

# Crear el deck con un estilo de mapa claro
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/streets-v11"  # Estilo de mapa claro
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(deck)

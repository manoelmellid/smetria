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

# Asegurarse de que las coordenadas sean de tipo float
df_activo['latitude'] = pd.to_numeric(df_activo['latitud'], errors='coerce')
df_activo['longitude'] = pd.to_numeric(df_activo['longitud'], errors='coerce')

# Función para ajustar el tamaño del punto en función del zoom
def adjust_point_size(zoom_level):
    # Define un rango de tamaño de los puntos
    min_size = 5
    max_size = 50
    
    # Ajusta el tamaño en función del zoom (nivel máximo de zoom en Mapbox es 15)
    size = min_size + (max_size - min_size) * (zoom_level / 15)
    return size

# Establece un valor de zoom por defecto
default_zoom = 12

# Crear la vista del mapa con el zoom inicial
view_state = pdk.ViewState(
    latitude=df_activo['latitude'].mean(),
    longitude=df_activo['longitude'].mean(),
    zoom=default_zoom,
    pitch=0,
    bearing=0
)

# Ajustar el tamaño del punto según el nivel de zoom inicial
point_size = adjust_point_size(view_state.zoom)

# Crea la capa para el mapa con el tamaño de punto dinámico
layer = pdk.Layer(
    'ScatterplotLayer',
    df_activo,
    get_position='[longitude, latitude]',
    get_radius=point_size,  # Tamaño dinámico del punto
    get_fill_color=[255, 0, 0, 160],  # Color del punto (rojo)
    pickable=True,
    auto_highlight=True
)

# Agregar etiquetas de texto (Tipo de incidencia) sobre los puntos
tooltip = {
    "html": "<b>Tipo:</b> {tipo_incidencia}",  # Mostrar el tipo de cada ubicación
    "style": {"color": "white", "backgroundColor": "rgba(0,0,0,0.7)", "padding": "5px"}
}

# Crear el deck con un estilo de mapa claro
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style="mapbox://styles/mapbox/streets-v11"  # Estilo de mapa claro
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(deck)

# Slider para ajustar el zoom manualmente
zoom_slider = st.slider("Ajusta el nivel de zoom", 0, 15, default_zoom)
view_state.zoom = zoom_slider

# Recalcular el tamaño del punto según el nuevo nivel de zoom
layer.data['size'] = adjust_point_size(view_state.zoom)

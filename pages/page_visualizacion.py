según el zoom
import streamlit as st
import pydeck as pdk
import pandas as pd

# Datos de ejemplo con coordenadas
data = pd.DataFrame({
    'lat': [37.7749, 34.0522, 40.7128],
    'lon': [-122.4194, -118.2437, -74.0060],
    'size': [100, 200, 300]  # Tamaños base de los puntos
})

# Función para ajustar el tamaño del punto en función del zoom
def adjust_point_size(zoom_level):
    # Define un rango de tamaño de los puntos
    min_size = 5
    max_size = 50
    
    # Ajusta el tamaño en función del zoom
    size = min_size + (max_size - min_size) * (zoom_level / 15)  # 15 es el nivel máximo de zoom en Mapbox
    return size

# Establece un valor de zoom por defecto
default_zoom = 10

# Crear la vista del mapa con el zoom
view_state = pdk.ViewState(
    latitude=37.7749,  # Coordenada central (San Francisco)
    longitude=-122.4194,
    zoom=default_zoom,
    pitch=0,
    bearing=0
)

# Crear la capa de puntos (scatterplot layer)
point_size = adjust_point_size(view_state.zoom)  # Ajustamos el tamaño según el zoom

layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position=["lon", "lat"],
    get_radius=point_size,  # Ajustamos el tamaño del punto
    get_fill_color=[255, 0, 0],  # Color de los puntos
    pickable=True,
    opacity=0.8,
)

# Configuración del mapa
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11"
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(deck)

# Opción para cambiar el zoom manualmente (para probar)
zoom_slider = st.slider("Ajusta el nivel de zoom", 0, 15, default_zoom)
view_state.zoom = zoom_slider


A este código, no toques nada de sus funcionalidades
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

# Crea la capa para el mapa
layer = pdk.Layer(
    'ScatterplotLayer',
    df_activo,
    get_position='[longitude, latitude]',
    get_radius=50,  # Tamaño del punto
    get_fill_color=[255, 0, 0, 160],  # Color del punto (rojo)
    pickable=True,
    auto_highlight=True
)

# Agregar etiquetas de texto (Tipo de incidencia) sobre los puntos
tooltip = {
    "html": "<b>Tipo:</b> {tipo_incidencia}",  # Mostrar el tipo de cada ubicación
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

import streamlit as st
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
st.error("Esta sección de SMETRIA está en desarrollo todavía")
st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")
  input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

import folium
import streamlit as st
from folium.plugins import MarkerCluster

# Crear un mapa
m = folium.Map(location=[20.0, 0.0], zoom_start=2)

# Crear un grupo de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Coordenadas de ejemplo y datos adicionales
coordinates = [
    {"lat": 20, "lon": 0, "info": "Punto 1: Coordenada 20, 0"},
    {"lat": 25, "lon": 5, "info": "Punto 2: Coordenada 25, 5"},
    {"lat": 30, "lon": 10, "info": "Punto 3: Coordenada 30, 10"}
]

# Función para añadir marcadores con Tooltips y Popups
def add_marker_with_dynamic_size(map, coordinates):
    for coord in coordinates:
        lat, lon, info = coord["lat"], coord["lon"], coord["info"]
        
        # Crear un marcador con un tamaño dinámico en función del zoom
        marker = folium.CircleMarker(
            location=[lat, lon], 
            radius=8, 
            color='blue', 
            fill=True, 
            fill_opacity=0.6
        )
        
        # Tooltip que aparece al pasar el ratón por encima
        marker.add_child(folium.Tooltip(info))
        
        # Popup que aparece al hacer clic en el marcador
        marker.add_child(folium.Popup(info))
        
        # Añadir el marcador al mapa
        marker.add_to(map)

# Añadir los marcadores
add_marker_with_dynamic_size(m, coordinates)

# Mostrar el mapa en Streamlit
st.components.v1.html(m._repr_html_(), height=500)




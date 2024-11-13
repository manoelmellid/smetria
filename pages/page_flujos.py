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

# Coordenadas de ejemplo
coordinates = [(20, 0), (25, 5), (30, 10)]

# Función para ajustar el tamaño de los puntos según el zoom
def add_marker_with_dynamic_size(map, coordinates):
    for lat, lon in coordinates:
        # Aquí el tamaño de los puntos depende de la escala del mapa
        marker = folium.CircleMarker(location=[lat, lon], radius=8, color='blue', fill=True, fill_opacity=0.6)
        marker.add_to(map)

# Añadir marcadores
add_marker_with_dynamic_size(m, coordinates)

# Mostrar el mapa en Streamlit
st.components.v1.html(m._repr_html_(), height=500)



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

import pandas as pd
import folium
import streamlit as st
from folium.plugins import MarkerCluster

# Cargar el archivo CSV
df = pd.read_csv("respuestas.csv")

# Filtrar solo los registros donde el estado es "Activo"
df_activo = df[df['estado'] == 'Activo']

# Calcular los límites geográficos de las ubicaciones (min y max de latitud y longitud)
min_lat = df_activo['latitud'].min()
max_lat = df_activo['latitud'].max()
min_lon = df_activo['longitud'].min()
max_lon = df_activo['longitud'].max()

# Calcular el centro del mapa (promedio de latitudes y longitudes)
center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2

# Calcular el zoom inicial basado en la distancia entre los puntos
# Vamos a calcular un zoom que garantice que todos los puntos estén visibles
# Este es un truco para ajustarlo dinámicamente. Podríamos calcular el zoom de manera manual
# pero folium no ofrece una función automática para ello.
map_zoom = 10  # Establecer un zoom básico
if (max_lat - min_lat) > 10 or (max_lon - min_lon) > 10:
    map_zoom = 5  # Si el rango geográfico es muy grande, usar un zoom menor
elif (max_lat - min_lat) < 2 and (max_lon - min_lon) < 2:
    map_zoom = 12  # Si el rango geográfico es pequeño, usar un zoom mayor

# Crear un mapa base centrado en el centro calculado
m = folium.Map(location=[center_lat, center_lon], zoom_start=map_zoom)

# Crear un grupo de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Función para añadir marcadores con Tooltips y Popups
def add_marker_with_dynamic_size(map, df):
    for _, row in df.iterrows():
        lat, lon = row['latitud'], row['longitud']
        fecha = row['fecha']
        tipo_incidencia = row['tipo_incidencia']
        
        # Crear un marcador con un tamaño dinámico en función del zoom
        marker = folium.CircleMarker(
            location=[lat, lon], 
            radius=8, 
            color='blue', 
            fill=True, 
            fill_opacity=0.6
        )
        
        # Tooltip que aparece al pasar el ratón por encima
        tooltip_text = f"Fecha: {fecha}\nTipo de Incidencia: {tipo_incidencia}"
        marker.add_child(folium.Tooltip(tooltip_text))
        
        # Popup que aparece al hacer clic en el marcador
        popup_text = f"Fecha: {fecha}<br>Tipo de Incidencia: {tipo_incidencia}"
        marker.add_child(folium.Popup(popup_text))
        
        # Añadir el marcador al mapa
        marker.add_to(map)

# Añadir los marcadores solo para los registros activos
add_marker_with_dynamic_size(m, df_activo)

# Mostrar el mapa en Streamlit
st.components.v1.html(m._repr_html_(), height=500)







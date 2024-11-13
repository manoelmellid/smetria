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
# Asume que el archivo CSV tiene el formato mencionado, ajusta el path si es necesario
df = pd.read_csv("respuestas.csv")

# Filtrar solo los registros donde el estado es "Activo"
df_activo = df[df['estado'] == 'Activo']

# Crear un mapa base
m = folium.Map(location=[20.0, 0.0], zoom_start=2)

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





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

# Crear un mapa base (cualquier coordenada inicial, luego ajustamos el zoom)
m = folium.Map(location=[20.0, 0.0], zoom_start=10)

# Crear un grupo de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Función para añadir marcadores con Tooltips y Popups
def add_marker_with_dynamic_size(map, df):
    # Lista para almacenar las coordenadas de todos los puntos
    bounds = []
    
    for _, row in df.iterrows():
        lat, lon = row['latitud'], row['longitud']
        tipo_incidencia = row['tipo_incidencia']
        tipo_alerta = row['tipo_alerta']
      
        if tipo_alerta == "Baja":
          color='yellow'
        elif tipo_alerta == "Media":
          color='orange'
        elif tipo_alerta == "Alta":
          color='red'
        else:
          color='blue'
          
        # Crear un marcador con un tamaño dinámico en función del zoom
        marker = folium.CircleMarker(
            location=[lat, lon], 
            radius=8, 
            color=color, 
            fill=True, 
            fill_opacity=0.6
        )
        
        # Tooltip que aparece al pasar el ratón por encima
        tooltip_text = f"Tipo de Incidencia: {tipo_incidencia}"
        marker.add_child(folium.Tooltip(tooltip_text))
        
        # Popup que aparece al hacer clic en el marcador
        #popup_text = f"tipo_alerta: {tipo_alerta}<br>Tipo de Incidencia: {tipo_incidencia}"
        #marker.add_child(folium.Popup(popup_text))
        
        # Añadir el marcador al mapa
        marker.add_to(map)
        
        # Añadir las coordenadas del punto a la lista de bounds
        bounds.append([lat, lon])
    
    # Ajustar el zoom y el centro para que se ajusten a todos los puntos
    if bounds:
        map.fit_bounds(bounds)

# Añadir los marcadores solo para los registros activos
add_marker_with_dynamic_size(m, df_activo)

# Mostrar el mapa en Streamlit
st.components.v1.html(m._repr_html_(), height=500)








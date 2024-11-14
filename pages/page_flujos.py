import streamlit as st
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
st.error("Esta sección de SMETRIA está en desarrollo todavía")
st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")
  #input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

# ---------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
from utils import consultas_camino as concam, rutas as rut
import folium
from folium.plugins import MarkerCluster

# Variables de longitud y latitud inicializadas como None
longitud = None
latitud = None
df_filtrado = None
seleccion = None

st.header("Herramientas de navegación")
st.write("### Parámetros de filtro")

# Función para cargar el archivo CSV de ubicaciones
@st.cache_data
def cargar_datos(file_path):
    df = pd.read_csv(file_path)
    return df

# Cargar el archivo CSV
file_path = "puntos_interes.csv"
df = cargar_datos(file_path)

# Convertir datos en un GeoDataFrame
df['geometry'] = df['geom'].apply(lambda x: Point(map(float, x.replace("POINT (", "").replace(")", "").split())))
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf['lat'] = gdf['geometry'].y
gdf['lon'] = gdf['geometry'].x

# Selección de tipo de ubicación
tipos = df['tipo'].unique()
tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[3] if len(tipos) > 3 else [])

# Campo de entrada para el km del Camino
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

# Barra deslizante para seleccionar el radio de distancia
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Obtener valor máximo de Km permitido desde la función
max_km_value = concam.query_max_km_value()

# Crear un formulario para procesar la búsqueda al enviar
with st.form(key='my_form'):
  submit_button = st.form_submit_button(label='Enviar')

# Usamos st.session_state para controlar el estado entre ejecuciones
if 'longitud' in st.session_state and 'latitud' in st.session_state:
  longitud = st.session_state.longitud
  latitud = st.session_state.latitud

if submit_button:
  # Procesar la ubicación solo si el botón es presionado
  longitud, latitud, concello_id, ubicacion = concam.procesar_ubicacion(input_text)

  # Guardar en session_state para mantener el estado entre interacciones
  st.session_state.longitud = longitud
  st.session_state.latitud = latitud

  if longitud is None and latitud is None:
    st.error("No se encontraron resultados para el valor de Km proporcionado.")
  else:
    # Filtrar el dataframe por tipo de ubicación seleccionado
    df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]

    # Calcular distancias
    punto_usuario = (latitud, longitud)
    df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(
      lambda x: geodesic(punto_usuario, (x.y, x.x)).km
    )
    df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]
    st.write(df_filtrado)

    # Crear el mapa base centrado en la ubicación del usuario
    m = folium.Map(location=[latitud, longitud], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    
    # Añadir marcadores para cada ubicación
    for _, row in df_filtrado.iterrows():
        lat, lon = row['lat'], row['lon']
        tipo_ubicacion = row['tipo']
        nombre = row['nome']
        distancia = row['distancia_km']
        
        # Color del marcador según el tipo de ubicación
        if tipo_ubicacion == tipos[0]:
            color = 'blue'
        elif tipo_ubicacion == tipos[1]:
            color = 'green'
        elif tipo_ubicacion == tipos[2]:
            color = 'purple'
        else:
            color = 'orange'
    
        # Crear marcador con Tooltip y Popup
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.6,
            tooltip=f"{nombre} - {distancia:.2f} km",
            popup=f"Ubicación: {nombre}<br>Tipo: {tipo_ubicacion}<br>Distancia: {distancia:.2f} km"
        ).add_to(marker_cluster)
    
    # Añadir un marcador rojo para la posición del usuario
    folium.Marker(
        location=[latitud, longitud],
        icon=folium.Icon(color='red', icon='user'),
        tooltip="Tu posición"
    ).add_to(m)
    
    # Mostrar el mapa en Streamlit (fuera del bucle for)
    st.components.v1.html(m._repr_html_(), height=500)
    seleccion = 1


else:
  st.warning("Por favor, introduce una distancia en kilómetros.")

# Recuperar df_filtrado de session_state, si está disponible
#df_filtrado = st.session_state.get('df_filtrado', None)

if seleccion is not None:
  rut.mostrar_seleccion(df_filtrado, latitud, longitud)

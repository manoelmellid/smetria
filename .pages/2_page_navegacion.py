import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import folium
from folium.plugins import MarkerCluster
from utils import rutas as rut, general as gen

# Diccionario global para los colores
COLOR_MAP = {
    'centro_saude': 'red',
    'desfibrilador': 'green',
    'vivendas_turisticas': 'blue',
    'farmacia': 'purple',
    'apartamentos': 'orange',
    'pensiones': 'darkblue',
    'hotel': 'black',
    'camping': 'brown',
    'albergues_turisticos': 'yellow',
    'turismo_rural': 'gray',
    'hospital': 'darkred',
    'oficina_turismo': 'lightblue'
}

# Función para obtener el color
def get_color(tipo):
    return COLOR_MAP.get(tipo, 'black')  # Color negro por defecto

# Definir la función para añadir marcadores al mapa
def add_marker_with_dynamic_size(map, df, latitud, longitud):
    bounds = []  # Lista para almacenar las coordenadas de todos los puntos

    for _, row in df.iterrows():
        lat, lon = row['latitud'], row['longitud']
        nome = row['nome']
        tipo = row['tipo']
        distancia = round(row['distancia_km'], 2)

        # Obtener el color del marcador
        color = get_color(tipo)

        # Añadir un marcador con círculo dinámico
        marker = folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.6
        )
        # Posición del usuario
        folium.Marker(
            location=[latitud, longitud],
            icon=folium.Icon(color='red', icon='user'),
            tooltip="Tu posición"
        ).add_to(m)

        marker.add_child(folium.Popup(f"{distancia} Km"))
        marker.add_child(folium.Tooltip(nome))
        marker.add_to(map)

        bounds.append([lat, lon])  # Añadir las coordenadas a los bounds

    # Ajustar el mapa para incluir todos los puntos
    if bounds:
        map.fit_bounds(bounds)


# Estado de la aplicación
if 'df_filtrado' not in st.session_state:
    st.session_state['df_filtrado'] = None
if 'longitud' not in st.session_state:
    st.session_state['longitud'] = None
if 'latitud' not in st.session_state:
    st.session_state['latitud'] = None
if 'camino' not in st.session_state:
    st.session_state['camino'] = None

# Encabezado de la aplicación
st.header("Herramientas de navegación")
st.write("### Parámetros de filtro")

# Seleccionar camino
camino, archivo, abrv = gen.camino()

# Cargar datos
def cargar_datos():
    return pd.read_csv("puntos_interes.csv")

df = cargar_datos()
df['geometry'] = df['geom'].apply(lambda x: Point(map(float, x.replace("POINT (", "").replace(")", "").split())))
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf['lat'] = gdf['geometry'].y
gdf['lon'] = gdf['geometry'].x

# Selección de tipo de ubicación
tipos = df['tipo'].unique()
tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[3] if len(tipos) > 3 else [])

# Parámetros de búsqueda
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Formulario de envío
with st.form(key='my_form'):
    submit_button = st.form_submit_button(label='Enviar')

# Procesar resultados
if submit_button and input_text:
    longitud, latitud, concello_id, ubicacion, km_camino = gen.procesar_ubicacion(input_text, archivo)
    if longitud and latitud:
        st.session_state.longitud = longitud
        st.session_state.latitud = latitud
        punto_usuario = (latitud, longitud)

        # Filtrar el dataframe por tipo y calcular distancias
        df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]
        df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(
            lambda x: geodesic(punto_usuario, (x.y, x.x)).km
        )
        df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]
        st.session_state['df_filtrado'] = df_filtrado
    else:
        st.error("No se encontraron resultados para el valor de Km proporcionado.")

# Crear círculos con nombres como elementos HTML
circles_with_labels_html = "".join(
    f"""
    <div style='display: flex; align-items: center; margin: 0 10px;'>
        <div style='width: 20px; height: 20px; border-radius: 50%; background-color: {color}; margin-right: 8px;'></div>
        <span style='font-size: 14px;'>{name.replace('_', ' ').capitalize()}</span>
    </div>
    """
    for name, color in COLOR_MAP.items()
)

# Mostrar los círculos y nombres en una línea
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; align-items: center; flex-wrap: wrap;'>
        {circles_with_labels_html}
    </div>
    """,
    unsafe_allow_html=True
)

# Mostrar resultados
if st.session_state['df_filtrado'] is not None:
    m = folium.Map(location=[st.session_state.latitud, st.session_state.longitud], zoom_start=12)
    add_marker_with_dynamic_size(m, st.session_state['df_filtrado'], st.session_state.latitud, st.session_state.longitud)
    st.components.v1.html(m._repr_html_(), height=500)
    rut.mostrar_seleccion(st.session_state['df_filtrado'], st.session_state.latitud, st.session_state.longitud)
else:
    st.warning("Por favor, introduce una distancia en kilómetros.")

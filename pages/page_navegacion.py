import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import pydeck as pdk
from utils import consultas_camino as concam, pronostico as prn

# Variables de longitud y latitud inicializadas como None
longitud = None
latitud = None

st.header("Herramientas de navegación")
st.write("### Parámetros de Filtro")

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
tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[3])

# Campo de entrada para el km del Camino
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

# Barra deslizante para seleccionar el radio de distancia
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Obtener valor máximo de Km permitido desde la función
max_km_value = concam.query_max_km_value()

# Crear un formulario para procesar la búsqueda al enviar
with st.form(key='my_form'):
    submit_button = st.form_submit_button(label='Enviar')

if submit_button:
    longitud, latitud, concello_id, ubicacion = prn.procesar_ubicacion(input_text)
    if longitud is None and latitud is None:
        st.write("No se encontraron resultados para el valor de Km proporcionado.")
    else:
        # Filtrar el dataframe por tipo de ubicación seleccionado
        df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]

        # Calcular distancias
        punto_usuario = (latitud, longitud)
        df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(
            lambda x: geodesic(punto_usuario, (x.y, x.x)).km
        )
        df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]

        # Crear datos para pydeck
        data_ubicaciones = df_filtrado[['lat', 'lon']].to_dict(orient='records')
        data_usuario = [{'lat': latitud, 'lon': longitud}]

        # Configurar el mapa con pydeck
        view_state = pdk.ViewState(
            latitude=latitud,
            longitude=longitud,
            zoom=12,
            pitch=0
        )

        # Capa para las ubicaciones
        ubicaciones_layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_ubicaciones,
            get_position='[lon, lat]',
            get_color='[0, 0, 255, 160]',  # Color azul
            get_radius=100,
            pickable=True  # Hacer que los puntos sean seleccionables
        )

        # Capa para el punto de usuario
        usuario_layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_usuario,
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 200]',  # Color rojo
            get_radius=150,
        )

        # Crear el mapa interactivo
        deck = pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=view_state,
            layers=[ubicaciones_layer, usuario_layer]
        )

        # Mostrar el mapa y capturar la selección del usuario
        selected = st.pydeck_chart(deck)

        # Si hay una selección, guardar en session_state y mostrar los detalles
        if selected:
            st.session_state.selected_point = selected[0]  # Guardar el primer punto seleccionado
            # Acceder a la fila correspondiente en el DataFrame usando el índice
            indice = st.session_state.selected_point['index']
            punto_info = df_filtrado.iloc[indice]
            st.write(f"Información sobre el punto seleccionado:")
            st.write(f"Nombre: {punto_info['nome']}")
            st.write(f"Dirección: {punto_info['enderezo']}")
            st.write(f"Distancia desde tu ubicación: {punto_info['distancia_km']:.2f} km")
else:
    st.warning("Por favor, introduce una distancia en kilómetros.")

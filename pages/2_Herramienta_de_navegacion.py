import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic

st.set_page_config(page_title="Herramienta de navegacion")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()
st.header("Herramienta de navegacion geospacial")

# ---------------------------------------------------------
st.sidebar.header("Parámetros de Filtro")

# Función para cargar el archivo CSV de ubicaciones
@st.cache_data
def cargar_ubicaciones():
    # Cargar el archivo CSV (asegúrate de que el archivo esté en el directorio o provee la ruta correcta)
    df = pd.read_csv("puntos_interes.csv")
    
    # Conversión de datos en un GeoDataFrame para facilitar cálculos de distancia
    df['geometry'] = df['geom'].apply(lambda x: Point(map(float, x.replace("POINT (", "").replace(")", "").split())))
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    
    return gdf

# Cargar las ubicaciones utilizando la función definida
gdf = cargar_ubicaciones()

# Selección del tipo de ubicación
tipos = gdf['tipo'].unique()
tipo_seleccionado = st.sidebar.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[0])

# Entrada de coordenadas y radio de distancia
latitud = st.sidebar.number_input("Latitud", value=43.0, format="%.6f")
longitud = st.sidebar.number_input("Longitud", value=-8.0, format="%.6f")
radio_km = st.sidebar.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Filtrar el dataframe por tipo de ubicación seleccionado
df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]

# Filtrar por distancia
punto_usuario = (latitud, longitud)
df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(lambda x: geodesic(punto_usuario, (x.y, x.x)).km)
df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]

# Mostrar resultados en el mapa
st.write(f"### Ubicaciones dentro de {radio_km} km del punto especificado")
st.map(df_filtrado[['geometry']])

# Mostrar tabla con detalles de las ubicaciones
st.write(df_filtrado[['id', 'tipo', 'nome', 'distancia_km']].sort_values(by='distancia_km'))

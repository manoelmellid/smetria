import streamlit as st
import pandas as pd
from shapely.geometry import Point
from geopy.distance import geodesic

# Configuración de la página
st.set_page_config(page_title="Herramienta de navegación", page_icon="📍")

# Encabezado e imagen
col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()
st.header("Herramienta de navegación geospacial")

# Parámetros de filtro en la barra lateral
st.sidebar.header("Parámetros de Filtro")

# Función para cargar el archivo CSV de ubicaciones
@st.cache_data
def cargar_datos(file_path):
    df = pd.read_csv(file_path)
    return df

# Cargar el archivo CSV
file_path = "puntos_interes.csv"  # Asegúrate de que el archivo esté en el directorio o provee la ruta correcta
df = cargar_datos(file_path)

# Extraer coordenadas de la columna 'geom' sin geopandas
def extraer_coordenadas(geom):
    coords = geom.replace("POINT (", "").replace(")", "").split()
    return float(coords[0]), float(coords[1])

df['longitud'], df['latitud'] = zip(*df['geom'].apply(extraer_coordenadas))

# Selección del tipo de ubicación
tipos = df['tipo'].unique()
tipo_seleccionado = st.sidebar.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[0])

# Entrada de coordenadas y radio de distancia
latitud_usuario = st.sidebar.number_input("Latitud", value=43.0, format="%.6f")
longitud_usuario = st.sidebar.number_input("Longitud", value=-8.0, format="%.6f")
radio_km = st.sidebar.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Filtrar el dataframe por tipo de ubicación seleccionado
df_filtrado = df[df['tipo'].isin(tipo_seleccionado)]

# Filtrar por distancia
punto_usuario = (latitud_usuario, longitud_usuario)
df_filtrado['distancia_km'] = df_filtrado.apply(
    lambda row: geodesic(punto_usuario, (row['latitud'], row['longitud'])).km, axis=1
)
df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]

# Mostrar resultados en el mapa
st.write(f"### Ubicaciones dentro de {radio_km} km del punto especificado")
st.map(df_filtrado[['latitud', 'longitud']])

# Mostrar tabla con detalles de las ubicaciones
st.write(df_filtrado[['id', 'tipo', 'nome', 'distancia_km']].sort_values(by='distancia_km'))

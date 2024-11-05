import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
from utils import consultas_camino as concam

# Variables de longitud y latitud inicializadas como None
longitud = None
latitud = None

st.set_page_config(page_title="Herramienta de Navegación")

# Configurar las columnas para el diseño
col1, col2, col3 = st.columns([3, 3, 3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Herramientas de navegación")
st.header("Parámetros de Filtro")

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
tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[0])

# Campo de entrada para el km del Camino
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

# Barra deslizante para seleccionar el radio de distancia
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Obtener valor máximo de Km permitido desde la función
max_km_value = concam.query_max_km_value()

# Crear un formulario para procesar la búsqueda al enviar
with st.form(key='my_form'):
    submit_button = st.form_submit_button(label='Enviar')

# Solo ejecutar el código si se ha presionado el botón 'Enviar'
if submit_button:
    if input_text:
        try:
            input_km = float(input_text)

            if input_km > max_km_value:
                st.warning(f"El valor {input_km} es mayor que el máximo permitido: {max_km_value}.")
            else:
                km_camino = float(input_text.replace(',', '.'))
                n = int(km_camino)

                # Calcular el valor ajustado basado en el rango
                if km_camino == max_km_value:
                    resultado = km_camino
                elif n < km_camino < n + 0.25:
                    resultado = n + 0.25
                elif n + 0.25 < km_camino < n + 0.5:
                    resultado = n + 0.5
                elif n + 0.5 < km_camino < n + 0.75:
                    resultado = n + 0.75
                elif n + 0.75 < km_camino < n + 1:
                    resultado = n + 1
                else:
                    resultado = km_camino

                # Consultar datos y actualizar variables
                longitud, latitud, concello_id, ubicacion = concam.query_csv_data(resultado)

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

                    # Mostrar resultados en el mapa
                    st.write(f"### Ubicaciones dentro de {radio_km} km del punto especificado")
                    st.map(df_filtrado[['lat', 'lon']])

                    # Mostrar tabla con detalles
                    st.write(df_filtrado[['id', 'tipo', 'nome', 'distancia_km']].sort_values(by='distancia_km'))
        except ValueError:
            st.error("Por favor, ingresa un número válido.")
    else:
        st.warning("Por favor, introduce una distancia en kilómetros.")

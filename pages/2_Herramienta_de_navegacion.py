import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
from utils import consultas_camino as concam

longitud = None
latitud = None

st.set_page_config(page_title="Herramienta de Navegacion")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Herramientas de navegación")
# Aquí incluirías todo el código específico para la predicción
st.header("Parámetros de Filtro")

# Función para cargar el archivo CSV de ubicaciones
@st.cache_data
def cargar_datos(file_path):
    df = pd.read_csv(file_path)
    return df

# Cargar el archivo CSV (asegúrate de que el archivo esté en el directorio o provee la ruta correcta)
file_path = "puntos_interes.csv"  # Reemplaza con la ruta de tu archivo si es necesario
df = cargar_datos(file_path)

# Conversión de datos en un GeoDataFrame para facilitar cálculos de distancia
df['geometry'] = df['geom'].apply(lambda x: Point(map(float, x.replace("POINT (", "").replace(")", "").split())))
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Extraer latitud y longitud para uso en el mapa
gdf['lat'] = gdf['geometry'].y
gdf['lon'] = gdf['geometry'].x

# Selección del tipo de ubicación
tipos = df['tipo'].unique()
tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", tipos, default=tipos[0])

max_km_value = concam.query_max_km_value()

with st.form(key='my_form'):
    # Entradas del formulario
    input_text = st.text_input("Indica el Km del Camino dónde te encuentras")

    # Botón para enviar el formulario
    submit_button = st.form_submit_button(label='Enviar')

    # Verifica si el campo de texto no está vacío solo después de que se presiona el botón
    if submit_button:
        try:
            # Convertir el input a un número
            input_km = float(input_text)

            # Comparar el valor de input con el máximo
            if input_km > max_km_value:
                st.warning(f"El valor {input_km} es mayor que el máximo permitido: {max_km_value}.")
        except ValueError:
            st.error("Por favor, ingresa un número válido.")

        if input_text:
            km_camino = float(input_text.replace(',', '.'))
            n = int(km_camino)

            if km_camino == max_km_value:
                resultado = km_camino  # Mantiene el valor igual si es igual a max_km_value
            elif n < km_camino < n + 0.25:
                resultado = n + 0.25
            elif n + 0.25 < km_camino < n + 0.5:
                resultado = n + 0.5
            elif n + 0.5 < km_camino < n + 0.75:
                resultado = n + 0.75
            elif n + 0.75 < km_camino < n + 1:
                resultado = n + 1
            else:
                resultado = km_camino  # Si no está en ningún rango, devuelve el número original

            # Actualiza las variables con los resultados de la función
            longitud, latitud, concello_id, ubicacion = concam.query_csv_data(resultado)
            adelante = 1

            # Imprimir las coordenadas
            if longitud is None and latitud is None:
                st.write("No se encontraron resultados para el valor de Km proporcionado.")
                
        else:
            st.warning("Por favor, introduce una distancia en kilómetros.")

# Entrada de coordenadas y radio de distancia
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Filtrar el dataframe por tipo de ubicación seleccionado
df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]

# Filtrar por distancia
punto_usuario = (latitud, longitud)
df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(lambda x: geodesic(punto_usuario, (x.y, x.x)).km)
df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]

# Mostrar resultados en el mapa
st.write(f"### Ubicaciones dentro de {radio_km} km del punto especificado")
st.map(df_filtrado[['lat', 'lon']])

# Mostrar tabla con detalles de las ubicaciones
st.write(df_filtrado[['id', 'tipo', 'nome', 'distancia_km']].sort_values(by='distancia_km'))

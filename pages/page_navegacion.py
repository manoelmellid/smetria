import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import pydeck as pdk
from utils import consultas_camino as concam

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

if submit_button:
    longitud, latitud, concello_id, ubicacion = concam.procesar_ubicacion(input_text)
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

        # Definir un diccionario de colores para cada tipo de ubicación
        colores_limitados = [
            [0, 255, 255],    # Cian
            [0, 255, 0],      # Verde
            [0, 0, 255],      # Azul
            [255, 255, 0],    # Amarillo
            [128, 0, 128],    # Púrpura
            [0, 128, 128],    # Teal
            [255, 165, 0],    # Naranja
            [255, 105, 180],  # Rosa
            [34, 139, 34],    # Verde oscuro
            [75, 0, 130],     # Índigo
            [240, 230, 140]   # Amarillo claro
        ]
        
        color_por_tipo = {
            tipos[i]: color for i, color in enumerate(colores_limitados[:len(tipos)])
        }

        # Añadir una columna de color al DataFrame según el tipo de ubicación
        df_filtrado['color'] = df_filtrado['tipo'].map(lambda tipo: color_por_tipo.get(tipo, [255, 255, 255]))


        # Crear datos para pydeck, incluyendo el color
        data_ubicaciones = df_filtrado[['lat', 'lon', 'color']].to_dict(orient='records')
        data_usuario = [{'lat': latitud, 'lon': longitud}]

        # Configurar el mapa con pydeck
        view_state = pdk.ViewState(
            latitude=latitud,
            longitude=longitud,
            zoom=12,
            pitch=0
        )

        # Capa para las ubicaciones con colores dinámicos
        ubicaciones_layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_ubicaciones,
            get_position='[lon, lat]',
            get_color='color',  # Usar la columna de color
            get_radius=100,
        )

        # Capa para el punto de usuario
        usuario_layer = pdk.Layer(
            'ScatterplotLayer',
            data=data_usuario,
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 200]',  # Color rojo para el usuario
            get_radius=150,
        )

        # Renderizar el mapa
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=view_state,
            layers=[ubicaciones_layer, usuario_layer]
        ))

        # Create the HTML table for results
        table_html = """
            <style>
                .result-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .result-table th, .result-table td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                .result-table th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                .color-box {
                    width: 30px;
                    height: 30px;
                    display: inline-block;
                }
            </style>
            <table class="result-table">
                <tr>
                    <th>Nombre</th>
                    <th>Distancia</th>
                    <th>Color</th>
                </tr>
        """
        
        # Generate table rows from filtered DataFrame
        for _, row in df_filtrado[['nome', 'distancia_km', 'color']].iterrows():
            color_html = f'rgb({row["color"][0]}, {row["color"][1]}, {row["color"][2]})'
            table_html += f"""
                <tr>
                    <td>{row['nome']}</td>
                    <td>{row['distancia_km']:.2f} km</td>
                    <td><div class="color-box" style="background-color: {color_html};"></div></td>
                </tr>
            """
        
        # Close the table HTML
        table_html += "</table>"
        
        # Display the table
        st.markdown(table_html, unsafe_allow_html=True)
else:
    st.warning("Por favor, introduce una distancia en kilómetros.")

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import folium
from folium.plugins import MarkerCluster
from utils import consultas_camino as concam, rutas as rut, general as gen

# Inicializa variables en session_state al inicio
st.session_state['busqueda'] = False
if 'longitud' not in st.session_state:
    st.session_state['longitud'] = None
    st.session_state['latitud'] = None
    st.session_state['busqueda'] = False
    st.session_state['df_filtrado'] = None

# Header
st.header("Herramientas de navegación")
st.write("### Parámetros de filtro")

# Selección de camino
camino = gen.camino()
if camino == "Camino Portugués":
    archivo = "vertices_250_camino_pt.csv"
elif camino in ["Camino Francés", "Camino Inglés", "Camino del Norte"]:
    archivo = "vertices_250_camino_pt.csv"
    st.warning(f"La función específica del {camino} aún está en desarrollo, se utilizará el Portugués, gracias.")
    camino = "Camino Portugués"

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

# Entrada de parámetros de búsqueda
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")
radio_km = st.slider("Radio de distancia (km)", min_value=1, max_value=10, value=5)

# Formulario de búsqueda
with st.form(key='search_form'):
    submit_button = st.form_submit_button(label='Buscar')

# Procesar búsqueda al enviar
if submit_button:
    longitud, latitud, _, _, _ = concam.procesar_ubicacion(input_text, archivo)
    if longitud and latitud:
        st.session_state['longitud'] = longitud
        st.session_state['latitud'] = latitud
        st.session_state['busqueda'] = True
        punto_usuario = (latitud, longitud)
        
        # Filtrar por tipo y calcular distancias
        df_filtrado = gdf[gdf['tipo'].isin(tipo_seleccionado)]
        df_filtrado['distancia_km'] = df_filtrado['geometry'].apply(
            lambda x: geodesic(punto_usuario, (x.y, x.x)).km
        )
        df_filtrado = df_filtrado[df_filtrado['distancia_km'] <= radio_km]
        st.session_state['df_filtrado'] = df_filtrado
    else:
        st.error("No se encontraron resultados para el valor de Km proporcionado.")

# Mostrar resultados si se realizó la búsqueda
if st.session_state['busqueda'] and st.session_state['df_filtrado'] is not None:
    st.write(st.session_state['df_filtrado'])

    # Crear un mapa con marcadores
    def mostrar_mapa(df, latitud, longitud):
        m = folium.Map(location=[latitud, longitud], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in df.iterrows():
            lat, lon = row['lat'], row['lon']
            tipo = row['tipo']
            distancia = round(row['distancia_km'], 2)
            
            # Define color según el tipo
            color = {
                'centro_saude': 'red',
                'desfibrilador': 'green',
                'vivendas_turisticas': 'blue',
                'farmacia': 'purple',
                'apartamentos': 'orange',
                'pensiones': 'darkblue',
                'hotel': 'pink',
                'camping': 'brown',
                'albergues_turisticos': 'yellow',
                'turismo_rural': 'gray',
                'hospital': 'darkred',
                'oficina_turismo': 'lightblue'
            }.get(tipo, 'black')

            # Añadir marcadores
            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(color=color),
                tooltip=f"{row['nome']} ({distancia} km)"
            ).add_to(marker_cluster)

        # Posición del usuario
        folium.Marker(
            location=[latitud, longitud],
            icon=folium.Icon(color='red', icon='user'),
            tooltip="Tu posición"
        ).add_to(m)

        # Mostrar el mapa
        st.components.v1.html(m._repr_html_(), height=500)

    mostrar_mapa(st.session_state['df_filtrado'], st.session_state['latitud'], st.session_state['longitud'])

    # Mostrar selección de lugar
    def mostrar_seleccion(df):
        df['nombre_con_distancia'] = df['nome'] + ' - ' + df['distancia_km'].round(3).astype(str) + ' km'
        opcion_seleccionada = st.selectbox('Selecciona un lugar', df['nombre_con_distancia'])

        if st.button("Calcular ruta"):
            nombre_seleccionado = opcion_seleccionada.split(' - ')[0]
            fila_seleccionada = df[df['nome'] == nombre_seleccionado].iloc[0]
            destino = [fila_seleccionada['lon'], fila_seleccionada['lat']]
            origen = [st.session_state['longitud'], st.session_state['latitud']]

            # Mostrar ruta
            st.write(f"Ruta desde tu posición hasta {nombre_seleccionado}.")
            # Aquí puedes añadir código adicional para mostrar un mapa con la ruta
            # usando bibliotecas como Folium o Pydeck.

    mostrar_seleccion(st.session_state['df_filtrado'])

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import pydeck as pdk
import folium
from folium.plugins import MarkerCluster
from utils import consultas_camino as concam, rutas as rut, general as gen

# Variables de longitud y latitud inicializadas como None
longitud = None
latitud = None
df_filtrado = None

st.header("Herramientas de navegación")
st.write("### Parámetros de filtro")

camino = gen.camino()
if camino == "Camino Portugués":
    archivo = "vertices_250_camino_pt.csv"
elif camino == "Camino Francés":
    archivo = "vertices_250_camino_pt.csv"
    st.warning(f"La función especifica del {camino} aún está en desarrollo, se utilizará el Portugués, gracias.")
    camino = "Camino Portugués"
elif camino == "Camino Inglés":
    st.warning(f"La función especifica del {camino} aún está en desarrollo, se utilizará el Portugués, gracias.")
    archivo = "vertices_250_camino_pt.csv"
    camino = "Camino Portugués"
elif camino == "Camino del Norte":
    st.warning(f"La función especifica del {camino} aún está en desarrollo, se utilizará el Portugués, gracias.")
    archivo = "vertices_250_camino_pt.csv"
    camino = "Camino Portugués"

# Cargar el archivo CSV
def cargar_datos():
    return pd.read_csv("puntos_interes.csv")
df = cargar_datos()

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

# Crear un formulario para procesar la búsqueda al enviar
with st.form(key='my_form'):
    submit_button = st.form_submit_button(label='Enviar')

# Usamos st.session_state para controlar el estado entre ejecuciones
if 'longitud' in st.session_state and 'latitud' in st.session_state:
    longitud = st.session_state.longitud
    latitud = st.session_state.latitud

if submit_button:
    # Procesar la ubicación solo si el botón es presionado
    longitud, latitud, concello_id, ubicacion, km = concam.procesar_ubicacion(input_text, archivo)

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
        
        m = folium.Map(location=[20.0, 0.0], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(m)

        def add_marker_with_dynamic_size(map, df):
            # Lista para almacenar las coordenadas de todos los puntos
            bounds = []
            
            for _, row in df.iterrows():
                lat, lon = row['latitud'], row['longitud']
                nome = row['nome']
                tipo = row['tipo']

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
                popup_text = f"Km {km}"
                marker.add_child(folium.Popup(popup_text))
                
                # Añadir el marcador al mapa
                marker.add_to(map)
                
                # Añadir las coordenadas del punto a la lista de bounds
                bounds.append([lat, lon])
        
            # Ajustar el zoom y el centro para que se ajusten a todos los puntos
            if bounds:
                map.fit_bounds(bounds)
    
        # Añadir los marcadores solo para los registros flitrados
        add_marker_with_dynamic_size(m, df_filtrado)
        
        # Mostrar el mapa en Streamlit
        st.components.v1.html(m._repr_html_(), height=500)

else:
    st.warning("Por favor, introduce una distancia en kilómetros.")

# Recuperar df_filtrado de session_state, si está disponible
df_filtrado = st.session_state.get('df_filtrado', None)

if df_filtrado is not None:
    rut.mostrar_seleccion(df_filtrado, latitud, longitud)

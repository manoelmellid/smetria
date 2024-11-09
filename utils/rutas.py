import openrouteservice
import streamlit as st
import pydeck as pdk
import json

def mostrar_seleccion(df, latitud_ori, longitud_ori):
    # Crear una nueva columna combinando 'nome' y 'distancia_km' para mostrar en el desplegable
    df['nombre_con_distancia'] = df['nome'] + ' - ' + df['distancia_km'].round(3).astype(str) + ' km'
    
    # Mostrar un desplegable con los valores de 'nombre_con_distancia'
    opcion_seleccionada = st.selectbox('Selecciona un lugar', df['nombre_con_distancia'])
    
    if st.button("Calcular ruta"):
        if opcion_seleccionada:
            # Extraer el nombre de la opción seleccionada (antes del "-")
            nombre_seleccionado = opcion_seleccionada.split(' - ')[0]
            
            # Filtrar la fila correspondiente al nombre seleccionado
            fila_seleccionada = df[df['nome'] == nombre_seleccionado].iloc[0]
            
            # Extraer latitud, longitud y distancia
            lat = fila_seleccionada['lat']
            lon = fila_seleccionada['lon']
            distancia = fila_seleccionada['distancia_km']
            
            # Mostrar los valores
            st.write(f'#### Mostrando ruta hasta {nombre_seleccionado}')
            # Definir las coordenadas de origen y destino
            origen = [longitud_ori, latitud_ori]
            destino = [lon, lat]
            mostrar_mapa(origen, destino)

# Función para obtener la ruta a pie entre dos puntos
def obtener_ruta_a_pie(api_key, origen, destino):
    client = openrouteservice.Client(key=api_key)
    
    try:
        ruta = client.directions(
            coordinates=[origen, destino],
            profile='foot-walking',
            format='geojson',
            radiuses=[1000, 1000]  # Intentar aumentar el radio
        )
        return ruta
    except openrouteservice.exceptions.ApiError as e:
        st.error("Error al obtener la ruta: " + str(e))
        return None

# Función para mostrar el mapa con la ruta
def mostrar_mapa(origen, destino):
    # Obtener el token de Streamlit secrets
    api_key = st.secrets["openrouteservice"]["api_key"]
    
    # Obtener la ruta a pie
    ruta = obtener_ruta_a_pie(api_key, origen, destino)
    
    # Extraer las coordenadas de la ruta
    coords = ruta['features'][0]['geometry']['coordinates']
    
    # Definir la vista inicial del mapa centrada entre los dos puntos
    centro = [(origen[1] + destino[1]) / 2, (origen[0] + destino[0]) / 2]
    vista = pdk.ViewState(
        latitude=centro[0],
        longitude=centro[1],
        zoom=14  # Nivel de zoom inicial
    )
    
    # Crear la capa de ruta (polyline)
    ruta_capa = pdk.Layer(
        "PathLayer",
        data=[{
            'coordinates': coords,
            'color': [255, 0, 0],  # Color rojo para la ruta
            'width': 15  # Grosor inicial de la línea (esto se ajustará según el zoom)
        }],
        get_path='coordinates',
        get_color='color',
        get_width='width',
        width_scale=0.5  # Este valor ajusta cómo cambia el grosor con el zoom
    )
    
    # Crear una capa de marcadores para el origen y destino
    puntos_capa = pdk.Layer(
        "ScatterplotLayer",
        data=[{
            'position': origen,
            'color': [0, 255, 0],  # Verde para el origen
            'radius': 30  # Tamaño del marcador de origen
        }, {
            'position': destino,
            'color': [0, 0, 255],  # Azul para el destino
            'radius': 30  # Tamaño del marcador de destino
        }],
        get_position='position',
        get_color='color',
        get_radius='radius'
    )
    
    # Crear el mapa con las capas y el zoom adaptativo
    deck = pdk.Deck(
        layers=[ruta_capa, puntos_capa],
        initial_view_state=vista,
        map_style="mapbox://styles/mapbox/streets-v11",
    )
    
    # Mostrar el mapa en streamlit
    st.pydeck_chart(deck)

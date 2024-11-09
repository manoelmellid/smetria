import openrouteservice
import streamlit as st
import pydeck as pdk
import json

# Función para obtener la ruta a pie entre dos puntos
def obtener_ruta_a_pie(api_key, origen, destino):
    client = openrouteservice.Client(key=api_key)
    
    try:
        ruta = client.directions(
            coordinates=[origen, destino],
            profile='driving-car',
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
    
    # Crear una capa de ruta (polyline)
    ruta_capa = pdk.Layer(
        "PathLayer",
        data=[{
            'coordinates': coords,
            'color': [255, 0, 0],  # Color rojo para la ruta
            'width': 5
        }],
        get_path='coordinates',
        get_color='color',
        get_width='width',
        width_scale=20
    )
    
    # Crear una capa de marcadores para el origen y destino
    puntos_capa = pdk.Layer(
        "ScatterplotLayer",
        data=[{
            'position': origen,
            'color': [0, 255, 0],  # Verde para el origen
            'radius': 200
        }, {
            'position': destino,
            'color': [0, 0, 255],  # Azul para el destino
            'radius': 200
        }],
        get_position='position',
        get_color='color',
        get_radius='radius'
    )

    # Definir la vista inicial del mapa centrada entre los dos puntos
    centro = [(origen[1] + destino[1]) / 2, (origen[0] + destino[0]) / 2]
    vista = pdk.ViewState(
        latitude=centro[0],
        longitude=centro[1],
        zoom=14
    )
    
    # Crear el mapa con las capas
    deck = pdk.Deck(
        layers=[ruta_capa, puntos_capa],
        initial_view_state=vista,
        map_style="mapbox://styles/mapbox/streets-v11",
    )
    
    # Mostrar el mapa en streamlit
    st.pydeck_chart(deck)

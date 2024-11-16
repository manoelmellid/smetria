import openrouteservice
import streamlit as st
import pydeck as pdk
import json

def mostrar_seleccion(df, latitud_ori, longitud_ori):
    # Crear una nueva columna combinando 'nome' y 'distancia_km' para mostrar en el desplegable
    df['nombre_con_distancia'] = df['nome'] + ' - ' + df['distancia_km'].round(3).astype(str) + ' km'
    
    # Mostrar un desplegable con los valores de 'nombre_con_distancia'
    opcion_seleccionada = st.selectbox('Selecciona un lugar', df['nome'])
    
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

import folium
from folium import PolyLine, Marker

import folium
from folium import PolyLine, Marker

# Función para mostrar el mapa con la ruta usando Folium
def mostrar_mapa(origen, destino):
    bounds = []  # Lista para almacenar los límites de los puntos
    
    # Obtener el token de Streamlit secrets
    api_key = st.secrets["openrouteservice"]["api_key"]
    
    # Obtener la ruta a pie
    ruta = obtener_ruta_a_pie(api_key, origen, destino)
    
    # Extraer las coordenadas de la ruta
    coords = ruta['features'][0]['geometry']['coordinates']
    coords = [(lat, lon) for lon, lat in coords]  # Cambiar el orden a (lat, lon) para Folium
    
    # Agregar los puntos de la ruta a los bounds
    bounds.extend(coords)
    
    # Definir el centro del mapa entre el origen y el destino
    centro = [(origen[1] + destino[1]) / 2, (origen[0] + destino[0]) / 2]
    
    # Crear el mapa centrado
    m = folium.Map(location=centro, zoom_start=14, tiles="OpenStreetMap")
    
    # Agregar la ruta al mapa como una línea poligonal
    PolyLine(
        locations=coords,
        color="red",  # Color de la línea
        weight=5,  # Grosor de la línea
        opacity=0.8  # Opacidad de la línea
    ).add_to(m)
    
    # Agregar un marcador para el punto de origen
    Marker(
        location=[origen[1], origen[0]],  # Latitud y longitud
        icon=folium.Icon(color="green", icon="home"),
        popup="Inicio de la ruta"
    ).add_to(m)
    
    # Agregar un marcador para el punto de destino
    Marker(
        location=[destino[1], destino[0]],  # Latitud y longitud
        icon=folium.Icon(color="blue", icon="flag"),
        popup="Destino"
    ).add_to(m)
    
    # Agregar el origen y destino a los bounds
    bounds.append((origen[1], origen[0]))
    bounds.append((destino[1], destino[0]))
    
    # Ajustar el mapa para incluir todos los puntos
    if bounds:
        m.fit_bounds(bounds)
    
    # Mostrar el mapa en Streamlit
    st.components.v1.html(m._repr_html_(), height=500)

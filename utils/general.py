import streamlit as st
import pydeck as pdk

def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
    
    # Si no está logueado, el sistema solo permitirá el login si el usuario es admin
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        # Obtener las credenciales de st.secrets
        admin_username = st.secrets["admin_username"]
        admin_password = st.secrets["admin_password"]
        
        if st.button("Iniciar sesión"):
            # Solo se permite login para el admin
            if username == admin_username and password == admin_password:
                st.session_state.logged_in = True
                st.session_state.role = 'admin'
                st.success("Bienvenido, Administrador")
            else:
                st.session_state.logged_in = False
    return st.session_state.logged_in

# Función para crear el mapa

def mostrar_puntos_con_arcos(latitud, longitud, altura_columna=500):
    # Puntos predefinidos, ahora usando un diccionario con las coordenadas
    puntos = [
        {"name": "Tui", "lon": -8.647561062369814, "lat": 42.03689869234378},
        {"name": "Porriño", "lon": -8.621155902537511, "lat": 42.161771976830565},
        {"name": "Redondela", "lon": -8.608127425736257, "lat": 42.28321455965748},
        {"name": "Ponte Sampaio", "lon": -8.60739744888831, "lat": 42.34692538060731},
        {"name": "Pontevedra", "lon": -8.64485792166723, "lat": 42.43147462464597},
        {"name": "Caldas de Rei", "lon": -8.643032777153794, "lat": 42.60372324695396},
        {"name": "Padrón", "lon": -8.661625079278618, "lat": 42.738909894811925},
        {"name": "Milladoiro", "lon": -8.580879782625436, "lat": 42.844542908024806},
        {"name": "Santiago de Compostela", "lon": -8.54365852835325, "lat": 42.8805986746478},
    ]

    # Agregar el punto adicional sin nombre
    punto_adicional = {"lon": longitud, "lat": latitud}

    # Crear las líneas de arco solo entre los puntos predefinidos
    arcos = []
    for i in range(len(puntos) - 1):
        lat1, lon1 = puntos[i]["lat"], puntos[i]["lon"]
        lat2, lon2 = puntos[i + 1]["lat"], puntos[i + 1]["lon"]
        arcos.append({
            "source": [lon1, lat1],
            "target": [lon2, lat2],
            "outbound": 100  # Ancho de la línea (puedes ajustarlo)
        })

    # Agregar la capa del arco
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arcos,
        get_source_position="source",
        get_target_position="target",
        get_source_color=[200, 30, 0, 160],
        get_target_color=[200, 30, 0, 160],
        auto_highlight=True,
        width_scale=0.0001,
        get_width="outbound",
        width_min_pixels=3,
        width_max_pixels=30,
    )

    # Crear la capa de la columna para el punto adicional
    columna_layer = pdk.Layer(
        "ColumnLayer",
        data=[{
            "lat": latitud,
            "lon": longitud,
            "elevation": altura_columna
        }],
        get_position=["lon", "lat"],
        get_elevation="elevation",
        elevation_scale=5,  # Escala de la columna
        radius=200,
        get_fill_color=[255, 0, 0, 140],  # Color rojo
    )

    # Capa de texto para mostrar los nombres de los puntos predefinidos
    text_layer = pdk.Layer(
        "TextLayer",
        data=puntos,
        get_position=["lon", "lat"],
        get_text="name",  # Esta es la clave que contiene el nombre del lugar
        get_size=10,  # Tamaño del texto
        get_color=[0, 0, 0, 255],  # Color del texto (negro)
        get_angle=0,  # Ángulo del texto (0 para horizontal)
        get_text_anchor="'middle'",  # Alineación del texto
        get_alignment_baseline="'center'",  # Alineación vertical
    )

    # No agregar texto para el punto adicional (solo lo mostramos como un punto sin nombre)
    text_layer_adicional = pdk.Layer(
        "TextLayer",
        data=[{
            "lon": longitud,
            "lat": latitud,
        }],
        get_position=["lon", "lat"],
        get_text="name",  # No se usa nombre para el punto adicional
        get_size=0,  # Sin texto visible
        get_color=[255, 0, 0, 0],  # Transparente (sin color visible)
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
    )

    # Configuración del mapa
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": latitud,
            "longitude": longitud,
            "zoom": 10,
            "pitch": 50,
        },
        layers=[arc_layer, columna_layer, text_layer, text_layer_adicional],
    )

    # Mostrar el mapa en Streamlit
    st.pydeck_chart(deck)

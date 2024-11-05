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
    # Puntos predefinidos
    puntos = [
        ("Tui", -8.647561062369814, 42.03689869234378),
        ("Porriño", -8.621155902537511, 42.161771976830565),
        ("Redondela", -8.608127425736257, 42.28321455965748),
        ("Ponte Sampaio", -8.60739744888831, 42.34692538060731),
        ("Pontevedra", -8.64485792166723, 42.43147462464597),
        ("Caldas de Rei", -8.643032777153794, 42.60372324695396),
        ("Padrón", -8.661625079278618, 42.738909894811925),
        ("Milladoiro", -8.580879782625436, 42.844542908024806),
        ("Santiago de Compostela", -8.54365852835325, 42.8805986746478),
    ]

    # Agregar el punto recibido como argumento
    punto_adicional = ("Punto Adicional", longitud, latitud)

    # Crear las líneas de arco solo entre los puntos predefinidos
    arcos = []
    for i in range(len(puntos) - 1):
        lat1, lon1 = puntos[i][2], puntos[i][1]
        lat2, lon2 = puntos[i + 1][2], puntos[i + 1][1]
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

    # Configuración del mapa
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": latitud,
            "longitude": longitud,
            "zoom": 10,
            "pitch": 50,
        },
        layers=[arc_layer, columna_layer],
    )

    # Mostrar el mapa en Streamlit
    st.pydeck_chart(deck)

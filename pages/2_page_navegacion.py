# Diccionario global para los colores
COLOR_MAP = {
    'centro_saude': 'red',
    'desfibrilador': 'green',
    'vivendas_turisticas': 'blue',
    'farmacia': 'purple',
    'apartamentos': 'orange',
    'pensiones': 'darkblue',
    'hotel': 'black',
    'camping': 'brown',
    'albergues_turisticos': 'yellow',
    'turismo_rural': 'gray',
    'hospital': 'darkred',
    'oficina_turismo': 'lightblue'
}

# Función para obtener el color
def get_color(tipo):
    return COLOR_MAP.get(tipo, 'black')  # Color negro por defecto

# Definir la función para añadir marcadores al mapa
def add_marker_with_dynamic_size(map, df, latitud, longitud):
    bounds = []  # Lista para almacenar las coordenadas de todos los puntos

    for _, row in df.iterrows():
        lat, lon = row['latitud'], row['longitud']
        nome = row['nome']
        tipo = row['tipo']
        distancia = round(row['distancia_km'], 2)

        # Obtener el color del marcador
        color = get_color(tipo)

        # Añadir un marcador con círculo dinámico
        marker = folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_opacity=0.6
        )
        # Posición del usuario
        folium.Marker(
            location=[latitud, longitud],
            icon=folium.Icon(color='red', icon='user'),
            tooltip="Tu posición"
        ).add_to(m)

        marker.add_child(folium.Popup(f"{distancia} Km"))
        marker.add_child(folium.Tooltip(nome))
        marker.add_to(map)

        bounds.append([lat, lon])  # Añadir las coordenadas a los bounds

    # Ajustar el mapa para incluir todos los puntos
    if bounds:
        map.fit_bounds(bounds)

# Crear círculos con nombres como elementos HTML
circles_with_labels_html = "".join(
    f"""
    <div style='display: flex; align-items: center; margin: 0 10px;'>
        <div style='width: 20px; height: 20px; border-radius: 50%; background-color: {color}; margin-right: 8px;'></div>
        <span style='font-size: 14px;'>{name.replace('_', ' ').capitalize()}</span>
    </div>
    """
    for name, color in COLOR_MAP.items()
)

# Mostrar los círculos y nombres en una línea
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; align-items: center; flex-wrap: wrap;'>
        {circles_with_labels_html}
    </div>
    """,
    unsafe_allow_html=True
)

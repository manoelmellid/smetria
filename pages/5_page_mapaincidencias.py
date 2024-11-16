import streamlit as st
import pandas as pd
import folium
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
from utils import github as git, general as gen

st.header("Mapa de visualización de incidencias")
st.error("Esta sección de SMETRIA está en desarrollo todavía")
# ---------------------------------------------------------------------------------
camino = gen.camino()
if camino == "Camino Portugués":
    archivo = "vertices_250_camino_pt.csv"
    abrv = "PT"
    
elif camino == "Camino Francés":
    archivo = "vertices_250_camino_pt.csv"
    camino = "Camino Portugués"
    abrv = "FR"
    
elif camino == "Camino Inglés":
    archivo = "vertices_250_camino_pt.csv"
    camino = "Camino Portugués"
    abrv = "EN"

elif camino == "Camino del Norte":
    archivo = "vertices_250_camino_pt.csv"
    camino = "Camino Portugués"
    abrv = "NO"

# Cargar los datos con solo las columnas necesarias
df = git.cargar_datos(columnas_necesarias=['id', 'estado', 'fecha', 'camino', 'km', 'latitud', 'longitud', 'tipo_incidencia', 'tipo_alerta'])

# Filtrar solo los registros donde el estado es "Activo" y el camino es "PT"
df_activo = df[(df['estado'] == 'Activo') & (df['camino'] == abrv)]

# Crear un mapa base (cualquier coordenada inicial, luego ajustamos el zoom)
m = folium.Map(location=[20.0, 0.0], zoom_start=10)

# Crear un grupo de marcadores
marker_cluster = MarkerCluster().add_to(m)

# Función para añadir marcadores con Tooltips y Popups
def add_marker_with_dynamic_size(map, df):
    # Lista para almacenar las coordenadas de todos los puntos
    bounds = []
    
    for _, row in df.iterrows():
        lat, lon = row['latitud'], row['longitud']
        tipo_incidencia = row['tipo_incidencia']
        tipo_alerta = row['tipo_alerta']
        km = row['km']
      
        if tipo_alerta == "Baja":
          color='yellow'
        elif tipo_alerta == "Media":
          color='orange'
        elif tipo_alerta == "Alta":
          color='red'
        else:
          color='blue'
          
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

# Añadir los marcadores solo para los registros activos
add_marker_with_dynamic_size(m, df_activo)

# Mostrar el mapa en Streamlit
st.components.v1.html(m._repr_html_(), height=500)

# Configurar el tamaño de la figura
fig, ax = plt.subplots(figsize=(3, 1))

# Colores y etiquetas de los círculos
colors = ["yellow", "orange", "red"]
labels = ["Baja", "Media", "Alta"]

# Dibujar los círculos
for i, (color, label) in enumerate(zip(colors, labels)):
    # Reducir el tamaño del círculo (radio 0.2 en lugar de 0.3)
    circle = plt.Circle((i + 1, 1), 0.2, color=color, ec="black")
    ax.add_artist(circle)
    ax.text(i + 1, 0.4, label, ha="center", fontsize=10)

# Configurar el eje
ax.set_xlim(0.5, 3.5)
ax.set_ylim(0, 2)
ax.axis("off")  # Quitar los ejes

# Establecer la relación de aspecto igual para evitar óvalos
ax.set_aspect('equal')

# Mostrar la figura en Streamlit
st.pyplot(fig)

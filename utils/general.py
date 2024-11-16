import streamlit as st
import pydeck as pdk
import pandas as pd
import re

def camino():
    camino = st.selectbox('Selecciona el Camino de Santiago que estás recorriendo:', ['Camino Portugués', 'Camino Francés', 'Camino Inglés', 'Camino del Norte'])
    if camino == "Camino Portugués":
        archivo = "vertices_250_camino_pt.csv"
        abrv = "PT"
    elif camino == "Camino Francés":
        archivo = "vertices_250_camino_pt.csv"
        st.warning(f"La función específica del {camino} aún está en desarrollo. Se utilizará el Portugués.")
        camino = "Camino Portugués"
        abrv = "FR"
    elif camino in ["Camino Inglés"]:
        st.warning(f"La función específica del {camino} aún está en desarrollo. Se utilizará el Portugués.")
        archivo = "vertices_250_camino_pt.csv"
        camino = "Camino Portugués"
        abrv = "EN"
    elif camino == "Camino del Norte":
        st.warning(f"La función específica del {camino} aún está en desarrollo. Se utilizará el Portugués.")
        archivo = "vertices_250_camino_pt.csv"
        camino = "Camino Portugués"
        abrv = "NO"
    return camino, archivo, abrv
    
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
            else:
                st.error("Contraseña o usuario incorrectos")
                st.session_state.logged_in = False
    return st.session_state.logged_in
    
# Función para validar el número de teléfono
def validar_telefono(telefono):
    # Expresión regular para un formato de número de teléfono (ej. +34 612 345 678)
    patron = r"^\+?[0-9]{1,3}?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}$"
    if re.match(patron, telefono):
        return True
    return False

def query_csv_data(km_value, archivo):
    # Cargar el archivo CSV
    df = pd.read_csv(archivo)  # Asegúrate de que la ruta sea correcta

    # Filtrar los datos donde la columna 'km' es igual a km_value
    filtered_df = df[df['km'] == km_value][['longitud', 'latitud', 'concello_id', 'ubicacion']]
    
    # Verificar si el DataFrame filtrado no está vacío
    if not filtered_df.empty:
        # Retornar el primer elemento de cada columna como flotante, excepto concello_id y ubicacion
        longitud = float(filtered_df['longitud'].iloc[0])  # Convertir a float
        latitud = float(filtered_df['latitud'].iloc[0])    # Convertir a float
        concello_id = filtered_df['concello_id'].iloc[0]   # Texto
        ubicacion = filtered_df['ubicacion'].iloc[0]       # Texto
        return longitud, latitud, concello_id, ubicacion
    else:
        # Si no se encuentra el km_value, retornar None para los valores de longitud y latitud
        return None, None, None, None

def query_max_km_value(archivo):
    # Cargar el archivo CSV
    df = pd.read_csv(archivo)  # Asegúrate de que la ruta sea correcta

    # Verificar si el DataFrame no está vacío
    if not df.empty:
        # Obtener el valor máximo de la columna 'km'
        max_km_value = df['km'].max()
        return max_km_value
    else:
        # Si el DataFrame está vacío, retornar None
        return None

def procesar_ubicacion(input_text, archivo):
    max_km_value = query_max_km_value(archivo)
    if not input_text:
        print("Por favor, introduce una distancia en kilómetros.")
        return None, None, None, None  # Valores predeterminados cuando no hay input

    try:
        input_km = float(input_text.replace(',', '.'))  # Convierte el input a un número flotante
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return None, None, None, None

    # Verifica si el valor de km excede el máximo permitido
    if input_km > max_km_value:
        print(f"El valor {input_km} es mayor que el máximo permitido: {max_km_value}.")
        return None, None, None, None

    # Ajusta el valor de `km_camino` según las reglas dadas
    km_camino = input_km
    n = int(km_camino)

    if km_camino == max_km_value:
        resultado = km_camino
    elif n < km_camino < n + 0.25:
        resultado = n + 0.25
    elif n + 0.25 < km_camino < n + 0.5:
        resultado = n + 0.5
    elif n + 0.5 < km_camino < n + 0.75:
        resultado = n + 0.75
    elif n + 0.75 < km_camino < n + 1:
        resultado = n + 1
    else:
        resultado = km_camino

    # Consulta el CSV usando el resultado ajustado
    longitud, latitud, concello_id, ubicacion = query_csv_data(resultado, archivo)

    # Si no se encontraron resultados, devuelve una advertencia
    if longitud is None and latitud is None:
        print("No se encontraron resultados para el valor de Km proporcionado.")
        return None, None, None, None

    return longitud, latitud, concello_id, ubicacion, km_camino

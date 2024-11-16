import streamlit as st
import pandas as pd

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

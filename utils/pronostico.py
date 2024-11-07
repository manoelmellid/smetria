import requests
import json
from datetime import datetime, timedelta  # Corrige la importación
from utils import csv_json as cj, consultas_camino as concam
import streamlit as st
import os

API_KEY = st.secrets["API_KEY"]
base_url = 'https://servizos.meteogalicia.gal/apiv4/getNumericForecastInfo'

def pronostico(location_id, start_date, end_date):
    # Obtén la hora actual correctamente
    fecha_actual = datetime.now().date()

    if start_date == end_date:
        if start_date == fecha_actual:
            # Si el día es hoy, el tiempo empieza desde ahora + 1 hora hasta las 23:59
            start_date = datetime.now()
            end_date = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59)
        else:
            # Si es cualquier otro día, empieza desde las 0:00 hasta las 23:59 del día seleccionado
            start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    params = {
        'API_KEY': API_KEY,
        'locationIds': location_id,
        'startTime': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'endTime': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
        'lang': 'es',
        'tz': 'Europe/Madrid',
        'format': 'application/json'
    }

    # Realizar la solicitud a la API
    response = requests.get(base_url, params=params)

    # Comprobar si la respuesta es exitosa
    if response.status_code == 200:
        # Convertir a JSON y mostrar los datos
        forecast_data = response.json()
        print(f"Pronóstico para el ID {location_id} del {start_date} al {end_date}:")
        print(forecast_data)

        # Especifica el nombre del archivo donde se guardará el JSON
        nombre_archivo = 'forecast_data.json'  # Cambia aquí si es necesario

        # Guarda el diccionario en un archivo JSON
        try:
            with open(nombre_archivo, 'w') as archivo:
                json.dump(forecast_data, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

        # Convierte el JSON a CSV
        cj.json_to_csv(nombre_archivo, 'salida_forecast_data.csv')
    else:
        # En caso de error, mostrar mensaje de error
        print(f"Error: {response.status_code}")

def procesar_ubicacion(input_text):
    concam.max_km_value = concam.query_max_km_value()
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
    longitud, latitud, concello_id, ubicacion = concam.query_csv_data(resultado)

    # Si no se encontraron resultados, devuelve una advertencia
    if longitud is None and latitud is None:
        print("No se encontraron resultados para el valor de Km proporcionado.")
        return None, None, None, None

    return longitud, latitud, concello_id, ubicacion

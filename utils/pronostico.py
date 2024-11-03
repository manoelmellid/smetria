import requests
import json
from datetime import datetime, timedelta  # Corrige la importación
import csv_json as cj
import streamlit as st
import os

API_KEY = st.secrets["API_KEY"]
base_url = 'https://servizos.meteogalicia.gal/apiv4/getNumericForecastInfo'

def pronostico(location_id, start_date, end_date):
    # Obtén la hora actual correctamente
    hora_actual = datetime.now()

    if start_date.date() == end_date.date():
        if start_date.date() == fecha_actual:
            # Si el día es hoy, el tiempo empieza desde ahora + 1 hora hasta las 23:59
            hora_actual = datetime.now()
            start_date = hora_actual + timedelta(hours=1)
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

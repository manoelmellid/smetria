import pandas as pd
import streamlit as st

from utils import resumen_datos as redat

# Función para reorganizar temperaturas, precipitaciones y cielo y mostrar las tablas
def tabla_tiempo(archivo_csv):
    # Leer el archivo CSV
    df = pd.read_csv(archivo_csv)
    # Convertir la columna 'date_time' a formato de fecha y hora
    df['date_time'] = pd.to_datetime(df['date_time'])

    # Extraer los días únicos
    dias_unicos = df['date_time'].dt.date.unique()

    # Generar una tabla para cada día
    for dia in dias_unicos:
        # Filtrar el DataFrame por el día actual
        df_dia = df[df['date_time'].dt.date == dia]

        # Extraer la hora de la columna 'date_time'
        df_dia['hour'] = df_dia['date_time'].dt.hour

        # Ordenar los datos para que comiencen desde las 0:00
        df_dia = df_dia.sort_values(by='hour')

        # Crear listas con las horas, temperaturas, precipitaciones y estado del cielo
        horas = df_dia['hour'][:24].tolist()
        temperaturas = df_dia['temperature'][:24].tolist()
        precipitaciones = df_dia['precipitation_amount'][:24].tolist()
        estado_cielo = df_dia['sky_state'][:24].tolist()

        # Crear un DataFrame sin índices, donde la primera fila es la de horas
        tabla_reformateada = pd.DataFrame(
            {
                'Hora': horas,
                'Temperatura': temperaturas,
                'Precipitación': precipitaciones,
                'Estado del Cielo': estado_cielo
            }
        )

        # Transponer el DataFrame para cambiar filas por columnas y viceversa
        tabla_completa = tabla_reformateada.transpose()

        # Mapeo de estados del cielo a emoticonos
        emoticonos = {
            'SUNNY': '☀️',
            'HIGH_CLOUDS': '🌥️',
            'PARTLY_CLOUDY': '⛅',
            'OVERCAST': '☁️',
            'CLOUDY': '☁️',
            'FOG': '🌫️',
            'SHOWERS': '🌧️',
            'OVERCAST_AND_SHOWERS': '🌧️☁️',
            'INTERMITENT_SNOW': '🌨️',
            'DRIZZLE': '🌦️',
            'RAIN': '🌧️',
            'SNOW': '❄️',
            'STORMS': '⛈️',
            'MIST': '🌫️',
            'FOG_BANK': '🌁',
            'MID_CLOUDS': '🌥️',
            'WEAK_RAIN': '🌦️',
            'WEAK_SHOWERS': '🌦️',
            'STORM_THEN_CLOUDY': '⛈️☁️',
            'MELTED_SNOW': '☔',
            'RAIN_HAIL': '🌨️💧'
        }
        # Reemplazar estados del cielo por emoticonos
        # Asegurarse de aplicar el mapeo solo en la fila correspondiente
        tabla_completa.loc['Estado del Cielo'] = tabla_completa.loc['Estado del Cielo'].map(emoticonos)

        # Mostrar la tabla en Streamlit
        dia_formateado = dia.strftime('%d-%m_%Y')
        st.write(f"Pronóstico para el día: {dia_formateado}")
        redat.analizar_temperaturas(df_dia)
        st.dataframe(tabla_completa)

import pandas as pd
import streamlit as st

# Función para reorganizar temperaturas, precipitaciones y cielo y mostrar las tablas
def tabla_tiempo(archivo_csv):
    # Leer el archivo CSV
    df = pd.read_csv(archivo_csv)
    # Convertir la columna 'date_time' a formato de fecha y hora
    df['date_time'] = pd.to_datetime(df['date_time'])

    # Crear dos variables para la fecha de inicio y fin
    start_date = df['date_time'].min().date()
    end_date = df['date_time'].max().date()

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
        temperaturas = df_dia['temperature'][:24].tolist()
        precipitaciones = df_dia['precipitation_amount'][:24].tolist()
        estado_cielo = df_dia['sky_state'][:24].tolist()

        # Crear un DataFrame sin índices, donde la primera fila es la de horas
        tabla_reformateada = pd.DataFrame(
            {
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
            'FOG': '🌫️'
        }
        # Reemplazar estados del cielo por emoticonos
        # Asegurarse de aplicar el mapeo solo en la fila correspondiente
        tabla_completa.loc['Estado del Cielo'] = tabla_completa.loc['Estado del Cielo'].map(emoticonos)

        # Mostrar la tabla en Streamlit
        st.write(f"Datos para el día: {dia}")
        st.dataframe(tabla_completa)

# Llamar a la función desde el código principal
tabla_tiempo("salida_forecast_data.csv")

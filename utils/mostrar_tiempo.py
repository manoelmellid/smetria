import pandas as pd
import streamlit as st

# Diccionario de emoticonos para los estados del cielo
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

def analizar_temperaturas(df):
    # Convertir la columna 'temperature' a numérico
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

    # Filtrar valores NaN
    df = df.dropna(subset=['temperature'])

    # Obtener la lista de temperaturas
    temperaturas = df['temperature'].tolist()

    # Calcular el máximo y el mínimo
    maximo = max(temperaturas) if temperaturas else None
    minimo = min(temperaturas) if temperaturas else None

    return maximo, minimo

# Función para calcular el estado medio del cielo para cada día
def estado_medio_cielo(df, dia):
    # Filtrar los datos para la fecha especificada
    df_dia = df[df['date_time'].dt.date == dia]

    # Contar las ocurrencias de cada estado del cielo
    conteo_estados = df_dia['sky_state'].value_counts()

    # Obtener el estado del cielo más frecuente
    estado_medio = conteo_estados.idxmax()

    # Obtener el emoticono correspondiente al estado medio
    emoticono_estado_medio = emoticonos.get(estado_medio, '🌈')  # Emoticono por defecto si no se encuentra el estado

    return emoticono_estado_medio

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
        df_dia = df[df['date_time'].dt.date == dia]
        # Extraer la hora de la columna 'date_time'
        df_dia = df_dia.copy()
        df_dia['hour'] = df_dia['date_time'].dt.hour

        # Ordenar los datos para que comiencen desde las 0:00
        df_dia = df_dia.sort_values(by='hour')

        # Crear listas con las horas, temperaturas, precipitaciones y estado del cielo
        horas = [f"{h}:00" for h in df_dia['hour'][:24].tolist()]
        temperaturas = [f"{temp} º" for temp in df_dia['temperature'][:24].tolist()]
        precipitaciones = [f"{prec} lm²" for prec in df_dia['precipitation_amount'][:24].tolist()]
        estado_cielo = df_dia['sky_state'][:24].tolist()

        # Crear un DataFrame sin índices, donde la primera fila es la de horas
        tabla_reformateada = pd.DataFrame(
            {
                'Hora': horas,
                'Temperatura': temperaturas,
                'Precipitación': precipitaciones,
                'Estado del cielo': estado_cielo
            }
        )

        # Transponer el DataFrame para cambiar filas por columnas y viceversa
        tabla_completa = tabla_reformateada.transpose()

        # Reemplazar estados del cielo por emoticonos
        tabla_completa.loc['Estado del cielo'] = tabla_completa.loc['Estado del cielo'].map(emoticonos)

        # Obtener el estado medio del cielo para el día
        estado_cielo_medio = estado_medio_cielo(df, dia)

        # Mostrar la tabla en Streamlit
        dia_formateado = dia.strftime('%d-%m-%Y')
        st.write(f"#### Pronóstico para el día: {dia_formateado}")

        maximo, minimo = analizar_temperaturas(df_dia)

        col1, col2, col3 = st.columns([2, 2, 2])
        # Mostrar en la interfaz de Streamlit
        with col1:
            st.metric(label="Temperatura Máxima", value=f"{maximo}º")
        with col2:
            st.metric(label="Temperatura Mínima", value=f"{minimo}º")
        with col3:
            st.metric(label="Estado medio del cielo", value=f"{estado_cielo_medio}")
        
        # Mostrar la tabla en pantalla completa
        st.dataframe(tabla_completa, use_container_width=True)

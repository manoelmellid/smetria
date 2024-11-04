import csv
import streamlit as st
import pandas as pd

def temperaturas(archivo_csv):
    temperaturas = []

    # Leer el archivo CSV
    with open(archivo_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convertir la temperatura a float y agregar a la lista
            temperaturas.append(float(row['temperature']))

    # Calcular la media, el máximo y el mínimo
    maximo = max(temperaturas) if temperaturas else None
    minimo = min(temperaturas) if temperaturas else None

    st.write(f"Temperaura máxima: {maximo}")
    st.write(f"Temperaura minima: {minimo}")

import pandas as pd
import streamlit as st

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
    media = sum(temperaturas) / len(temperaturas) if temperaturas else None

    col1, col2, col3 = st.columns([2, 2, 2])
    
    # Mostrar en la interfaz de Streamlit
    with col1:
        st.metric(label="Temperatura Máxima", value=maximo)
    with col2:
        st.metric(label="Temperatura Mínima", value=minimo)
    with col3:
        st.metric(label="Temperatura Media", value=round(media, 2) if media is not None else None)

import csv
import streamlit as st
import pandas as pd

from utils import tabla_tiempo as ttiempo

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
    

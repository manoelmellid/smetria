import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils import general as gen, consultas_camino as concam, pronostico as prn, tabla_tiempo as ttiempo

st.header("Predicción meteorológica")
longitud = None
latitud = None
concello_id = None
ubicacion = None
adelante = None
start_date = None
end_date = None
days=None
# Entradas del formulario
input_text = st.text_input("Indica el Km del Camino dónde te encuentras")
today = datetime.datetime.now()

# Selección de fechas
d = st.date_input(
    "Selecciona el periodo de tiempo",
    (today, today + datetime.timedelta(days=4)),  # Por defecto
    today,
    today + datetime.timedelta(days=4),  # Fecha máxima
    format="DD/MM/YYYY",
)

# Comprobar si se seleccionaron dos fechas
if isinstance(d, tuple) and len(d) == 2:
    start_date, end_date = d
else:
    st.error("Por favor selecciona una fecha de inicio y de fin")

# Botón para enviar el formulario
with st.form(key='my_form'):
    submit_button = st.form_submit_button(label='Enviar')

# Obtener las coordenadas del punto kilometrico
if submit_button:
    longitud, latitud, concello_id, ubicacion = concam.procesar_ubicacion(input_text)
    adelante=1

if concello_id is not None:
    st.write(f"### Predicción para tu ubicación: {concello_id}")

if latitud is not None and longitud is not None:
    # Crear el DataFrame solo si ambos valores son válidos
    data = pd.DataFrame({
        'lat': [latitud],  # Mejor como lista
        'lon': [longitud]
    }, index=[0])  # Proporciona un índice

    col1, col2 = st.columns([2,2])
    #with col1:
        #gen.mostrar_puntos_con_arcos(latitud, longitud, altura_columna=500)
    #with col2:
        #st.map(data) # Mostrar el mapa solo si los datos son válidos

if adelante is not None and longitud is not None:
    # Pronostico
    prn.pronostico(ubicacion, start_date, end_date)

    # Tablas de horas
    ttiempo.tabla_tiempo("salida_forecast_data.csv")

    # Carga de los datos
    df = pd.read_csv("salida_forecast_data.csv")

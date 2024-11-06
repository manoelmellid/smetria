import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Predicción meteorológica")

from utils import general as gen, consultas_camino as concam, pronostico as prn, tabla_tiempo as ttiempo

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()

st.header("Predicción meteorológica")
longitud = None
latitud = None
concello_id = None
ubicacion = None
adelante = None
start_date = None
end_date = None
days=None

max_km_value = concam.query_max_km_value()

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

# Verifica si el campo de texto no está vacío solo después de que se presiona el botón
if submit_button:
    if input_text:
        try:
            input_km = float(input_text) # Convertir el input a un número
            
            if input_km > max_km_value: # Comparar el valor de input con el máximo
                st.warning(f"El valor {input_km} es mayor que el máximo permitido: {max_km_value}.")
        except ValueError:
            st.error("Por favor, ingresa un número válido.")
        
    if input_text:
        km_camino = float(input_text.replace(',', '.'))
        n = int(km_camino)
    
        if km_camino == max_km_value:
            resultado = km_camino  # Mantiene el valor igual si es igual a max_km_value
        elif n < km_camino < n + 0.25:
            resultado = n + 0.25
        elif n + 0.25 < km_camino < n + 0.5:
            resultado = n + 0.5
        elif n + 0.5 < km_camino < n + 0.75:
            resultado = n + 0.75
        elif n + 0.75 < km_camino < n + 1:
            resultado = n + 1
        else:
            resultado = km_camino  # Si no está en ningún rango, devuelve el número original
    
        # Actualiza las variables con los resultados de la función
        longitud, latitud, concello_id, ubicacion = concam.query_csv_data(resultado)
        adelante = 1
    
        # Imprimir las coordenadas
        if longitud is None and latitud is None:
            st.write("No se encontraron resultados para el valor de Km proporcionado.")
            
    else:
        st.warning("Por favor, introduce una distancia en kilómetros.")

if concello_id is not None:
    st.write(f"### Predicción para tu ubicación: {concello_id}")

if latitud is not None and longitud is not None:
    # Crear el DataFrame solo si ambos valores son válidos
    data = pd.DataFrame({
        'lat': [latitud],  # Mejor como lista
        'lon': [longitud]
    }, index=[0])  # Proporciona un índice

    col1, col2 = st.columns([2,2])
    with col1:
        gen.mostrar_puntos_con_arcos(latitud, longitud, altura_columna=500)
    with col2:
        st.map(data) # Mostrar el mapa solo si los datos son válidos

if adelante is not None and longitud is not None:
    # Pronostico
    prn.pronostico(ubicacion, start_date, end_date)

    # Tablas de horas
    ttiempo.tabla_tiempo("salida_forecast_data.csv")

    # Carga de los datos
    df = pd.read_csv("salida_forecast_data.csv")

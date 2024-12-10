import streamlit as st
import datetime
import pandas as pd
import numpy as np
import joblib
import holidays
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
st.error("Esta sección de SMETRIA está en desarrollo todavía")
st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")
  #input_text = st.text_input("Indica el Km del Camino dónde te encuentras")
  camino = gen.camino()
# ---------------------------------------------------------------------------------

hora = st.time_input(
    'Selecciona una hora', 
    value=datetime.time(9, 0),  # Hora predeterminada (9:00 AM)
    step=datetime.timedelta(hours=1)  # Paso de 1 hora
)

st.write(hora)
hora_numero = hora.hour  # Extrae solo la parte de la hora como número
st.write(hora_numero)


# Ejemplo de predicción
zone_id = 25069
date = '2024-03-02'
hour = 12

# Cargar el modelo
filename = f'sav/random_forest_model_{zone_id}.sav'
loaded_model = joblib.load(filename)
print(f"Modelo cargado desde {filename}")

# Cargar el escalador usado previamente
scaler_filename = f'sav/scaler_{zone_id}.sav'
scaler = joblib.load(scaler_filename)

# Funciones auxiliares que deben definirse
def get_part_of_day(hour):
    if 0 <= hour < 6:
        return 'early_morning'
    elif 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'night'

def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'

galicia_calendar = holidays.ES(prov='GA')

def verificar_festivo(fecha):
    return 1 if fecha in galicia_calendar else 0

# Cargar las columnas originales para asegurarse de que las predicciones se realicen correctamente
# Estas deben coincidir con las columnas utilizadas en el modelo entrenado
columns = ['zone_id', 'hour', 'day_of_week', 'month', 'part_of_day', 'season',
           'zone_hour_interaction', 'is_weekend', 'is_holiday',
           'day_season_interaction', 'zone_month_interaction']

# Función para predicciones
def predict_visitors(zone_id, date, hour):
    date = pd.Timestamp(date)
    
    # Crear el dataframe de entrada con las características necesarias
    input_data = pd.DataFrame(columns=columns)

    input_data['zone_id'] = [zone_id]
    input_data['hour'] = [hour]
    input_data['day_of_week'] = [date.dayofweek]
    input_data['month'] = [date.month]
    input_data['part_of_day'] = [get_part_of_day(hour)]
    input_data['part_of_day'] = input_data['part_of_day'].astype('category').cat.codes
    input_data['season'] = [get_season(date.month)]
    input_data['season'] = input_data['season'].astype('category').cat.codes
    input_data['zone_hour_interaction'] = [zone_id * hour]
    input_data['is_weekend'] = [1 if date.dayofweek in [5, 6] else 0]
    input_data['is_holiday'] = [verificar_festivo(date.date())]
    input_data['day_season_interaction'] = [date.dayofweek * input_data['season'].iloc[0]]
    input_data['zone_month_interaction'] = [zone_id * date.month]

    # Escalar los datos de entrada
    input_data_scaled = scaler.transform(input_data)

    # Realizar la predicción en escala logarítmica
    prediction_log = loaded_model.predict(input_data_scaled)

    # Revertir la transformación logarítmica
    prediction = np.expm1(prediction_log)  # Revertir logaritmo
    return round(np.round(prediction)[0])

predicted_visitors = predict_visitors(zone_id, date, hour)
print(f"\nPredicción para zona {zone_id}, fecha {date}, hora {hour}: {predicted_visitors} visitantes únicos\n")

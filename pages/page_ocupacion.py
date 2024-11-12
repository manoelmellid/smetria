import streamlit as st
import pandas as pd

st.header("Modelo predictivo de ocupación")

# ---------------------------------------------------------------------
st.error("Esta sección de SMETRIA está en desarrollo todavía")

# Cargar datos desde el archivo CSV
albergues_df = pd.read_csv("albergues_por_concello.csv")

# Crear el diccionario de albergues por concello a partir del DataFrame
albergues_por_concello = {}
for _, row in albergues_df.iterrows():
    concello = row["Concello"]
    albergue = row["Albergue"]
    if concello not in albergues_por_concello:
        albergues_por_concello[concello] = []
    albergues_por_concello[concello].append(albergue)

# Crear la lista de concellos a partir de las claves del diccionario
concellos = list(albergues_por_concello.keys())

# Primer desplegable para seleccionar el concello
tipo_opc = st.selectbox('Selecciona el concello:', concellos)

# Si se selecciona un concello, mostrar el desplegable con los albergues correspondientes
if tipo_opc in albergues_por_concello:
    albergues = albergues_por_concello[tipo_opc]
    albergue_selec = st.selectbox('Selecciona el albergue:', albergues)

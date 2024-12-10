import streamlit as st
import pandas as pd
import datetime
import joblib
import holidays

st.header("Modelo predictivo de ocupación")

# ---------------------------------------------------------------------

# Cargar datos desde el archivo CSV
albergues_df = pd.read_csv("albergues_por_concello.csv")

# Crear el diccionario de albergues por concello y el diccionario de provincias por albergue
albergues_por_concello = {}
albergues_por_provincia = {}

for _, row in albergues_df.iterrows():
    concello = row["Concello"]
    albergue = row["Albergue"]
    provincia = row["Provincia"]
    
    # Para el diccionario de concellos
    if concello not in albergues_por_concello:
        albergues_por_concello[concello] = []
    albergues_por_concello[concello].append(albergue)
    
    # Para el diccionario de provincias
    albergues_por_provincia[albergue] = provincia

# Crear la lista de concellos a partir de las claves del diccionario
concellos = list(albergues_por_concello.keys())

# Primer desplegable para seleccionar el concello
tipo_opc = st.selectbox('Selecciona el concello:', concellos)

# Si se selecciona un concello, mostrar el desplegable con los albergues correspondientes
if tipo_opc in albergues_por_concello:
    albergues = albergues_por_concello[tipo_opc]
    albergue_selec = st.selectbox('Selecciona el albergue:', albergues)

    # Mostrar la provincia correspondiente al albergue seleccionado
    provincia = albergues_por_provincia.get(albergue_selec)

# Fecha de hoy
today = datetime.date.today()

# Selección de solo un día
dia = st.date_input(
    "Selecciona el día",
    today,  # Por defecto selecciona el día de hoy
    min_value=today,  # Fecha mínima (hoy)
    format="DD/MM/YYYY",
)

if st.button("Enviar"):
    def predecir_ocupacion(dia, alojamiento, municipio, provincia):
        # Cargar modelo y codificadores
        rf = joblib.load('rf_model.sav')
        label_encoders = joblib.load('label_encoders.sav')
    
        # Crear una fila con los datos ingresados
        galicia_calendar = holidays.ES(prov='GA')
        nueva_fila = {
            'dia': pd.to_datetime(dia),
            'alojamiento': alojamiento,
            'municipio': municipio,
            'provincia': provincia
        }
    
        nueva_fila['estacion'] = 'Primavera' if nueva_fila['dia'].month in [3, 4, 5] else \
                                 'Verano' if nueva_fila['dia'].month in [6, 7, 8] else \
                                 'Otoño' if nueva_fila['dia'].month in [9, 10, 11] else 'Invierno'
    
        nueva_fila['trimestre'] = 'Trimestre1' if nueva_fila['dia'].month in [1, 2, 3] else \
                                  'Trimestre2' if nueva_fila['dia'].month in [4, 5, 6] else \
                                  'Trimestre3' if nueva_fila['dia'].month in [7, 8, 9] else 'Trimestre4'
    
        nueva_fila['mes'] = nueva_fila['dia'].month_name()
        nueva_fila['dia_semana'] = nueva_fila['dia'].day_name()
        nueva_fila['es_festivo'] = 1 if nueva_fila['dia'] in galicia_calendar else 0
        nueva_fila['temporada_alta'] = 1 if nueva_fila['dia'].month in [5, 6, 7, 8] else 0
        nueva_fila['festivo_temporada'] = nueva_fila['es_festivo'] * nueva_fila['temporada_alta']
        nueva_fila['cercano_a_festivo'] = 1 if any((nueva_fila['dia'] + pd.Timedelta(days=delta)) in galicia_calendar for delta in range(-2, 3)) else 0
        nueva_fila['fin_de_semana'] = 1 if nueva_fila['dia'].dayofweek >= 5 else 0
    
        nueva_fila = pd.DataFrame([nueva_fila]).drop(columns=['dia'], errors='ignore')
    
        # Codificar las columnas categóricas
        for col, encoder in label_encoders.items():
            if col in nueva_fila.columns:
                nueva_fila[col] = nueva_fila[col].map(
                    lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
                )
    
        # Reindexar columnas para asegurar compatibilidad con el modelo
        X = pd.DataFrame(columns=joblib.load('rf_model_columns.sav'))  # Cargar columnas usadas al entrenar el modelo
        nueva_fila = nueva_fila.reindex(columns=X.columns, fill_value=0)
    
        # Realizar la predicción
        prediccion = rf.predict(nueva_fila)
        return prediccion[0]

    col1, col2, col3 = st.columns([2,2,2])
    ocupacion = predecir_ocupacion(dia, albergue_selec, tipo_opc, provincia)
    st.write("## Predicción de ocupación:")
    if ocupacion == "Ocupacion muy reducida":
        color = "🟩"
        porcentaje = "0-20%"
    elif ocupacion == "Ocupacion moderada baja":
        color = "🟨"
        porcentaje = "21-40%"
    elif ocupacion == "Ocupacion media":
        color = "🟧"
        porcentaje = "41-60%"
    elif ocupacion == "Ocupacion moderada alta":
        color = "🟥"
        porcentaje = "61-80%"
    elif ocupacion == "Ocupacion moderada alta":
        color = "❌"
        porcentaje = "81-100%"

    col1, col2, col3 = st.columns([2, 2, 2])
    # Mostrar en la interfaz de Streamlit
    with col1:
        st.write(f"#### {ocupacion}")
    with col2:
        st.write(f"#### {porcentaje}")
    with col3:
        st.write(f"#### {color}")
    

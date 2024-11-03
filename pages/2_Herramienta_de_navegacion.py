import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Herramienta de navegacion")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.divider()
st.header("Herramienta de navegacion geospacial")

# Obtener la fecha de hoy
hoy = datetime.date.today()
# Calcular la fecha máxima (hoy + 3 días)
max_fecha = hoy + datetime.timedelta(days=3)

# Crear el selector de fecha
d = st.date_input(
    "Selecciona tu fecha de vacaciones:",
    hoy,  # Fecha predeterminada
    min_value=hoy,  # Fecha mínima
    max_value=max_fecha,  # Fecha máxima
    format="MM.DD.YYYY"  # Formato de la fecha
)

# Comprobar si se seleccionaron dos fechas
if isinstance(d, tuple) and len(d) == 2:
    start_date, end_date = d
    # Mostrar las fechas
    st.write("Start Date:", start_date)
    st.write("End Date:", end_date)
else:
    st.error("Por favor selecciona una fecha de inicio y de fin")

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


# Obtener la fecha actual y calcular el próximo año
today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

# Definir un valor predeterminado para las fechas
default_end_date = datetime.date(next_year, 1, 7)

# Usar date_input con una tupla para el rango de fechas
d = st.date_input(
    "Select your vacation for next year",
    (jan_1, default_end_date),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)

# Comprobar si se seleccionó un rango de fechas
if isinstance(d, tuple):
    start_date, end_date = d
else:
    start_date = d
    end_date = start_date  # Si solo se selecciona una fecha, usarla como fin

# Mostrar las fechas
st.write("Start Date:", start_date)
st.write("End Date:", end_date)

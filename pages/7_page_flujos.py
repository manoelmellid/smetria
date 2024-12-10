import streamlit as st
import datetime
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

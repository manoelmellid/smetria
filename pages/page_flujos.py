import streamlit as st
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")


st.title("Ruta a Pie entre dos Puntos")
longitud = -8.544889 # origen
latitud = 42.87797 # origen

# Definir las coordenadas de origen y destino
origen = [longitud, latitud]
destino = [-8.5457598, 42.8804666]  # longitud, latitud


# Mostrar el mapa con la ruta
rut.mostrar_mapa(origen, destino)

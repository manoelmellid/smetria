import streamlit as st
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------

st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")


st.title("Ruta a Pie entre dos Puntos")

# Definir las coordenadas de origen y destino
origen = [-33.4489, -70.6693]  # Santiago, Chile (Lat, Long)
destino = [-33.4637, -70.6483]  # Barrio Lastarria, Santiago, Chile (Lat, Long)

# Mostrar el mapa con la ruta
rut.mostrar_mapa(origen, destino)

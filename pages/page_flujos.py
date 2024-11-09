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
#origen = [42.87437814285766, -8.549401826001816]
#destino = [42.88046663836321, -8.545759761367778]
origen = [-8.5494018, 42.8743781]  # longitud, latitud
destino = [-8.5457598, 42.8804666]  # longitud, latitud


# Mostrar el mapa con la ruta
rut.mostrar_mapa(origen, destino)

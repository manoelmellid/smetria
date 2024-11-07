import streamlit as st

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

opciones = ['Albergue', 'Fecha']
tipo_opc = st.selectbox('Selecciona el tipo de incidencia:', opciones)

if tipo_opc == 'Albergue':
  albergues = ['Tui1', 'Tui2']
  albergue_selec = st.selectbox('Selecciona el tipo de incidencia:', albergues)

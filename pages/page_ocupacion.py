import streamlit as st

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

concellos = ['Albergue', 'Concello']
tipo_opc = st.selectbox('Selecciona el concello:', opciones)

if tipo_opc == 'Albergue':
  albergues = ['Tui1', 'Tui2']
  albergue_selec = st.selectbox('Selecciona el tipo de incidencia:', albergues)

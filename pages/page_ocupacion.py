import streamlit as st

st.header("Modelo predictivo de ocupacion")

# ---------------------------------------------------------------------

tipo_seleccionado = st.multiselect("Selecciona el tipo de ubicación", ['Caca', 'Culo'], default=tipos[3])

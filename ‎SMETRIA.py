import streamlit as st
st.cache_data.clear()

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.markdown("<h3 style='text-align: center;'>Sistema de monitorización de eventos en tramos</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Camino de Santiago - Camino Portugués</h3>", unsafe_allow_html=True)

pages = {
    "SMETRIA": [
        st.Page("pages/page_inicio.py", title="Inicio"),
        st.Page("pages/page_prediccion.py", title="Prediccion meteorologica"),
        st.Page("prueba_pagina2.py", title="Herramienta de navegacion"),],}
pg = st.navigation(pages)
pg.run()

st.divider()
# -------------------------------------------------------------------------------



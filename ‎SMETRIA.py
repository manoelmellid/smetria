import streamlit as st
st.cache_data.clear()

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_container_width=True)
with col3:
    st.header("SMETRIA")

st.markdown("<h3 style='text-align: center;'>Sistema de monitorización de eventos en tramos</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Camino de Santiago - Camino Portugués</h3>", unsafe_allow_html=True)
st.divider()

pages = {
    "Menú": [
        st.Page("pages/page_inicio.py", title="Inicio"),
        st.Page("pages/page_meteorologia.py", title="Predicción meteorologica"),
        st.Page("pages/page_navegacion.py", title="Herramienta de navegación"),
        st.Page("pages/page_ocupacion.py", title="Modelo predictivo de ocupación"),
        st.Page("pages/page_notificacion.py", title="Notificación de incidencias"),
        st.Page("pages/page_visualizacion.py", title="Mapa de incidencias"),
    ],
    "Área privada": [
        st.Page("pages/page_recepcion.py", title="Recepción de incidencias"),
        st.Page("pages/page_flujos.py", title="Modelo predictivo de flujos"),
    ],
}
pg = st.navigation(pages)
pg.run()

# -------------------------------------------------------------------------------

import streamlit as st
st.cache_data.clear()

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")

st.markdown("<h3 style='text-align: center;'>Sistema de monitorización de eventos en tramos</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Camino de Santiago - Camino Portugués</h3>", unsafe_allow_html=True)


st.divider()

st.write("""SMETRIA cuenta con 4 funcionalidades para el usuario, un sistema de predicción meteorológica, una herramienta de consultas
geospaciales, un modelo predictivo de flujos y un modelo predictivo de ocupación
""")

b1, b2, b3, b4 = st.columns([3,3,3,3])

with b1:
    if st.button("Predicción meteorológica"):
        st.markdown("""
            <div style="text-align: center;">
                <meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/Modelo_predictivo_de_flujos'>
                Redirigiendo a la página...
            </div>
        """, unsafe_allow_html=True)
with b2:
    if st.button("Navegación geoespacial"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/Herramienta_de_navegacion'>", unsafe_allow_html=True)
with b3:
    if st.button("Flujos"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/Modelo_predictivo_de_flujos'>", unsafe_allow_html=True)
with b4:
    if st.button("Ocupación hotelera"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/Modelo_predictivo_de_ocupacion'>", unsafe_allow_html=True)


st.divider()
st.write("""
Esta web se ha desarrollado en el marco de la asignatura Proxecto Integrador I, del Grao de Intelixencia Artificial 
de la Universidade de Santiago de Compostela.
""")

nom1, nom2, nom3 = st.columns([3,3,3])
with nom1:
    st.markdown("<p style='text-align: center;'>Manoel Mellid Losada</p>", unsafe_allow_html=True)
with nom2:
    st.markdown("<p style='text-align: center;'>Borja Puime Rodríguez</p>", unsafe_allow_html=True)
with nom3:
    st.markdown("<p style='text-align: center;'>Carolina Rey Conesa</p>", unsafe_allow_html=True)
    
seg1, seg2, seg3 = st.columns([3,3,3])
with seg2:
    st.markdown("<p style='text-align: center;'>3º Intelixencia Artificial - USC</p>", unsafe_allow_html=True)



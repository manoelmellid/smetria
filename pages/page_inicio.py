import streamlit as st

st.write("""SMETRIA cuenta con 4 funcionalidades para el usuario: un sistema de predicción meteorológica, una herramienta de consultas
geospaciales, notificación de incidencias y un modelo predictivo de ocupación. Además, el personal de gestión puede acceder a los 
reportes de incidencias y al modelo predictivo de flujos.
""")

b1, b2, b3, b4 = st.columns([3,3,3,3])

with b1:
    if st.button("Predicción meteorológica"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/page_meteorologia'>", unsafe_allow_html=True)
with b2:
    if st.button("Navegación geoespacial"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/page_navegacion'>", unsafe_allow_html=True)
with b3:
    if st.button("Ocupación hotelera"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/page_ocupacion'>", unsafe_allow_html=True)
with b4:
    if st.button("Notificación de incidencias"):
        st.markdown("<meta http-equiv='refresh' content='0; url=https://smetria.streamlit.app/page_notificacion'>", unsafe_allow_html=True)
        
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

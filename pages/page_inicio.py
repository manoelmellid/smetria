import streamlit as st

st.write("#### Descripción de la plataforma:")
st.write("""SMETRIA ofrece a sus usuarios cuatro funcionalidades clave:

Sistema de Predicción Meteorológica
Herramienta de Consultas Geoespaciales
Notificación de Incidencias
Modelo Predictivo de Ocupación""")
st.write("""Además, el personal de gestión dispone de acceso a un área privada que le permite consultar el modelo predictivo de flujos y 
revisar los reportes de incidencias, con la capacidad de activar y desactivar las incidencias reportadas según sea necesario.""")
st.write("#### Sobre el caso de uso")
st.write("""Desde AMTEGA se nos propuso un caso de uso que integraría la mayoría de las funciones recogidas en esta web, en la App existente 
del Camino de Santiago de la Xunta. Debido a la falta de tiempo, descartamos la integración en la App y AMTEGA aceptó la solución propuesta 
por nosotros, esta web.""")
st.write("""El objetivo de centrado en usabilidad por parte de los peregrinos, así como que la web sirviera para facilitar el mantenimiento
del Camino de Santiago por parte de la administración.""")

b1, b2, b3, b4 = st.columns([3,3,3,3])

with b1:
    if st.button("Predicción meteorológica"):
        st.switch_page("pages/page_meteorologia.py")
with b2:
    if st.button("Navegación geoespacial"):
        st.switch_page("pages/page_navegacion.py")
with b3:
    if st.button("Ocupación hotelera"):
        st.switch_page("pages/page_ocupacion.py")
with b4:
    if st.button("Notificación de incidencias"):
        st.switch_page("pages/page_notificacion.py")
        
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

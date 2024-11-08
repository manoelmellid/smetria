import streamlit as st

st.write("#### Descripción de la plataforma:")
st.write("""SMETRIA ofrece a sus usuarios cuatro funcionalidades clave:
st.write(
    "- Sistema de Predicción Meteorológica\n"
    "- Herramienta de Consultas Geoespaciales\n"
    "- Notificación de Incidencias\n"
    "- Modelo Predictivo de Ocupación"
)
st.write("""Además, el personal de gestión dispone de acceso a un área privada que le permite consultar el modelo predictivo de flujos y 
revisar los reportes de incidencias, con la capacidad de activar y desactivar las incidencias reportadas según sea necesario.""")

st.write("#### Caso de uso")
st.write("""La Agencia para la Modernización Tecnológica de Galicia (AMTEGA) nos propuso un caso de uso que integraría varias de las 
funcionalidades presentes en esta plataforma con la aplicación móvil existente del Camino de Santiago, gestionada por la Xunta de Galicia. 
No obstante, debido a limitaciones de tiempo, se decidió no proceder con la integración en la aplicación móvil. En su lugar, AMTEGA 
aceptó la solución propuesta: esta web.""")

st.write("""El objetivo principal de SMETRIA es optimizar la experiencia de los peregrinos, brindando herramientas útiles para su 
navegación y seguridad, y, al mismo tiempo, facilitar las tareas de mantenimiento y gestión del Camino de Santiago por parte de 
las autoridades competentes.""")

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

import streamlit as st

st.write("#### Descripción de la plataforma:")
st.write("SMETRIA ofrece a sus usuarios varias funcionalidades clave para mejorar la experiencia del peregrino:")
col1, b1, b2, col4 = st.columns([0.1, 4, 4, 0.1])
with b1:
    if st.button("Sistema de Predicción Meteorológica"):
        st.switch_page("pages/1_page_meteorologia.py")
    if st.button("Modelo Predictivo de Ocupación"):
        st.switch_page("pages/3_page_ocupacion.py")
with b2:
    if st.button("Herramienta de navegación geoespacial"):
        st.switch_page("pages/2_page_navegacion.py")
    if st.button("Notificación de incidencias en el Camino"):
        st.switch_page("pages/4_page_notificacion.py")
b5, b6, b7 = st.columns([2,2,2])
with b6:
    if st.button("Mapa de incidencias"):
        st.switch_page("pages/5_page_mapaincidencias.py")

st.write("\nPara el personal que gestiona los Caminos de Santiago, hemos desarrollado dos herramientas que agilizan su trabajo")
cl1, c1, c2, cl4 = st.columns([0.1, 4, 4, 0.1])
with c1:
    if st.button("Recepción de incidencias"):
            st.switch_page("pages/6_page_recepcion.py")
with c2:
    if st.button("Flujos de peregrinos"):
        st.switch_page("pages/7_page_flujos.py")
with cl4:
    if st.button("Puta puta puta celta")

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
        
st.write("#### Contexto de desarrollo:")
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

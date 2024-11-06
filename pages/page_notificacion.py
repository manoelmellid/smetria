import streamlit as st
import csv
from utils import general as gen

st.set_page_config(page_title="Notificación de incidencias")

col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.image("amtega_logo.png_2089811488.png", use_column_width=True)
with col3:
    st.header("SMETRIA")
st.divider()
st.header("Sistema de notificación de incidencias")

def guardar_en_archivo(nombre, email, mensaje):
    with open('contactos.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre, email, mensaje])

def visualizar_archivo():
    # Leer el archivo contactos.csv y cargarlo en una lista
    try:
        with open('contactos.csv', mode='r') as file:
            reader = csv.reader(file)
            datos = list(reader)
            if datos:
                # Crear un dataframe a partir de los datos y mostrarlo
                st.write("### Incidencias Registradas")
                st.dataframe(datos)  # Puedes usar st.table(datos) si no quieres la funcionalidad interactiva
            else:
                st.write("No hay datos disponibles.")
    except FileNotFoundError:
        st.write("El archivo contactos.csv no existe aún.")

col1, col2, col3 = st.columns([2,2,2])
with col2:
    st.session_state.logged_in = gen.login()
# ---------------------------------------------------
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == True:
    st.write("Bienvenido al área de personal.")
    visualizar_archivo()
else:
    # Campos del formulario
    nombre = st.text_input("Nombre")
    email = st.text_input("Correo electrónico")
    mensaje = st.text_area("Mensaje")
    # Usar la función cuando el formulario se envíe
    if st.button("Enviar"):
        if nombre and email and mensaje:
            guardar_en_archivo(nombre, email, mensaje)
            st.success("¡Mensaje guardado con éxito!")
        else:
            st.error("Por favor, llena todos los campos.")


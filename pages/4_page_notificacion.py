import streamlit as st
import joblib
import spacy
import pandas as pd
from utils import general as gen, github as git

# Cargar el modelo de spaCy para preprocesamiento
nlp = spacy.load("es_core_news_sm")

# Función para preprocesar texto
def preprocesar_texto(texto):
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

# Cargar el modelo entrenado y el vectorizador
modelo_svm = joblib.load('modelo_svm.sav')
vectorizador = joblib.load('vectorizador_tfidf.sav')

# Título de la aplicación
st.header("Sistema de notificación de incidencias")

# Leer las opciones de incidencias
opciones_df = pd.read_csv('opciones_incidencias.csv')

# Campos del formulario
nombre = st.text_input("Nombre y apellidos")
telefono = st.text_input("Teléfono")

if telefono:
    if not gen.validar_telefono(telefono):
        st.error("Por favor, ingrese un número de teléfono válido.")
    else:
        email = st.text_input("Correo electrónico")
        camino, archivo, abrv = gen.camino()
        input_text = st.text_input("Indique el Km del Camino dónde se encuentra")
        # Campo para el mensaje de incidencia
        comentario = st.text_area("Añada una descripción:")

# Preprocesamiento y clasificación del tipo de incidencia
if comentario:
    # Preprocesar el comentario ingresado
    comentario_preprocesado = preprocesar_texto(comentario)
    
    # Vectorizar el comentario usando el vectorizador cargado
    comentario_vectorizado = vectorizador.transform([comentario_preprocesado])
    
    # Hacer la predicción
    tipo_opc_predict = modelo_svm.predict(comentario_vectorizado)[0]
    
    # Mostrar el tipo de incidencia clasificada
    st.write(f"El tipo de incidencia se va a clasificar como: **{tipo_opc_predict}**")
    # Mensaje informativo
    st.info(
    "El tipo de incidencia ha sido clasificado **automáticamente** mediante un modelo predictivo basado en **inteligencia artificial**. "
    "Le recomendamos revisar la clasificación antes de proceder con el envío."
    )
    
    # Buscar la alerta asociada al tipo de incidencia clasificado
    alerta_opc = opciones_df.loc[opciones_df['tipo'] == tipo_opc_predict, 'alerta'].iloc[0]
else:
    tipo_opc_predict = None
    alerta_opc = None

# Botón para enviar la notificación
if st.button("Enviar"):
    if nombre and email and telefono and input_text and tipo_opc_predict:
        # Llamar a la función para guardar en GitHub
        git.guardar_respuesta_en_csv(
            nombre=nombre,
            telefono=telefono,
            email=email,
            input_text=input_text,
            tipo_opc=tipo_opc_predict,
            mensaje=comentario,
            alerta_opc=alerta_opc,
            archivo=archivo,
            abrv=abrv
        )
        st.success("Notificación enviada con éxito.")
    else:
        st.error("Por favor, cubra los campos obligatorios.")

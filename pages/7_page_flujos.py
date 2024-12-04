import streamlit as st
from utils import general as gen, rutas as rut

st.header("Modelo predictivo de flujos")
# ---------------------------------------------------------------------------------
st.error("Esta sección de SMETRIA está en desarrollo todavía")
st.session_state.logged_in = gen.login()
# Si está logueado, muestra las vistas según el rol
if st.session_state.logged_in == False:
  st.success("Bienvenido al área privada de Flujos - SMETRIA")
  #input_text = st.text_input("Indica el Km del Camino dónde te encuentras")
  camino = gen.camino()
# ---------------------------------------------------------------------------------

import streamlit as st
import joblib
import spacy

# Cargar modelo de spaCy para preprocesamiento
nlp = spacy.load("es_core_news_sm")

# Función para preprocesar texto
def preprocesar_texto(texto):
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

# Cargar el modelo entrenado y el vectorizador
modelo_svm = joblib.load('modelo_svm.sav')
vectorizador = joblib.load('vectorizador_tfidf.sav')

# Título de la aplicación
st.title("Clasificador de Incidencias")

# Campo de entrada para el comentario
comentario = st.text_input("Escribe el comentario aquí:")

if comentario:
    # Preprocesar el comentario ingresado
    comentario_preprocesado = preprocesar_texto(comentario)
    
    # Vectorizar el comentario usando el vectorizador cargado
    comentario_vectorizado = vectorizador.transform([comentario_preprocesado])
    
    # Hacer la predicción
    prediccion = modelo_svm.predict(comentario_vectorizado)
    
    # Mostrar la predicción
    st.write(f"El tipo de incidencia clasificada es: **{prediccion[0]}**")


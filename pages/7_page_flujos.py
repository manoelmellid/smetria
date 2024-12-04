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
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE

# Cargar modelo spaCy
nlp = spacy.load("es_core_news_sm")

# Función para preprocesar texto
def preprocesar_texto(texto):
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop])

# Configuración de la página
st.title("Clasificación de Incidencias")
st.write("Ingrese un comentario para clasificar el tipo de incidencia y ver la precisión del modelo.")

# Cargar y preprocesar datos
@st.cache(allow_output_mutation=True)
def cargar_y_entrenar_modelo():
    # Cargar datos
    df = pd.read_csv("/Users/manoelmelide/Documents/respuestas.csv")
    df['comentario'] = df['comentario'].apply(preprocesar_texto)
    X = df['comentario']
    y = df['tipo_incidencia']

    # Vectorizador TF-IDF
    vectorizador = TfidfVectorizer(ngram_range=(1, 2))
    X_tfidf = vectorizador.fit_transform(X)

    # Aplicar SMOTE
    smote = SMOTE(random_state=42)
    X_bal, y_bal = smote.fit_resample(X_tfidf, y)

    # Entrenar modelo SVM
    modelo_svm = SVC(kernel='sigmoid', C=2, gamma='scale', random_state=42)
    modelo_svm.fit(X_bal, y_bal)

    return modelo_svm, vectorizador

# Cargar modelo y vectorizador
modelo_svm, vectorizador = cargar_y_entrenar_modelo()

# Entrada del usuario
comentario = st.text_area("Comentario", placeholder="Escriba el detalle de la incidencia aquí...")

if st.button("Clasificar"):
    if comentario.strip():
        # Preprocesar y vectorizar comentario
        comentario_preprocesado = preprocesar_texto(comentario)
        comentario_tfidf = vectorizador.transform([comentario_preprocesado])
        
        # Hacer predicción
        prediccion = modelo_svm.predict(comentario_tfidf)
        
        # Mostrar resultados
        st.success(f"El tipo de incidencia es: **{prediccion[0]}**")
    else:
        st.warning("Por favor, ingrese un comentario válido.")

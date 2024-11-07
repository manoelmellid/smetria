import streamlit as st
import requests
import csv
import io
import base64
import uuid
import datetime
import pandas as pd
from utils import pronostico as prn

# Configuración de GitHub desde los secretos de Streamlit
github_token = st.secrets["github"]["github_token"]
repo = st.secrets["github"]["repo"]
file_path = st.secrets["github"]["file_path"]
url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

# Función para cargar el archivo CSV desde un URL público
@st.cache_data
def cargar_datos(url):
    # Cargar el archivo CSV desde la URL proporcionada
    df = pd.read_csv(url)
    
    # Filtrar solo las columnas necesarias
    columnas_necesarias = ['id', 'fecha', 'ubicacion', 'tipo_incidencia']
    df_filtrado = df[columnas_necesarias]
    
    return df_filtrado

def guardar_respuesta_en_csv(nombre, email, input_text, tipo_opc, mensaje):
    fecha = datetime.datetime.now()
    longitud, latitud, concello_id, ubicacion = prn.procesar_ubicacion(input_text)
    ubicacion = [latitud, longitud]
    # Generar un ID único para cada respuesta
    respuesta_id = str(uuid.uuid4())
    
    # Limpiar el mensaje de saltos de línea
    mensaje_limpio = mensaje.replace('\n', ' ').replace('\r', ' ')
    
    # Crear una nueva línea de datos para agregar al archivo
    nueva_fila = [respuesta_id, fecha, nombre, email, ubicacion, tipo_opc, mensaje_limpio]
    
    # Obtener el contenido actual del archivo (si existe)
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    # Leer el contenido actual o inicializar una lista de filas vacía
    if response.status_code == 200:
        # Decodificar el contenido del archivo base64
        file_info = response.json()
        content = io.StringIO(base64.b64decode(file_info['content']).decode('utf-8'))
        
        # Leer las filas existentes y agregarlas a una lista
        reader = csv.reader(content)
        filas = list(reader)
    else:
        # Inicializar encabezados si el archivo no existe
        filas = [['id', 'nombre', 'mail', 'tipo_opc', 'mensaje']]
    
    # Añadir la nueva fila
    filas.append(nueva_fila)
    
    # Escribir el contenido CSV actualizado en un buffer de texto
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(filas)
    content_encoded = base64.b64encode(output.getvalue().encode('utf-8')).decode('utf-8')
    
    # Subir el archivo actualizado a GitHub
    data = {
        "message": f"Guardar respuesta ID: {respuesta_id}",
        "content": content_encoded
    }
    if response.status_code == 200:
        data["sha"] = file_info["sha"]  # SHA actual del archivo en GitHub
    
    # Realizar la solicitud de actualización o creación
    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        print("Archivo CSV actualizado exitosamente en GitHub.")
    else:
        print(f"Error al actualizar el archivo en GitHub: {response.status_code} - {response.text}")

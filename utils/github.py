import streamlit as st
import requests
import csv
import io
import base64
import uuid
import datetime
import pandas as pd
from utils import consultas_camino as concam

# Configuración de GitHub desde los secretos de Streamlit
github_token = st.secrets["github"]["github_token"]
repo = st.secrets["github"]["repo"]
file_path = st.secrets["github"]["file_path"]
url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

@st.cache_data
def cargar_datos(columnas_necesarias=None):
    headers = {
        "Authorization": f"token {github_token}"
    }
    response = requests.get(url, headers=headers)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        content = response.json()
        
        # Obtener el contenido base64 del archivo CSV
        file_content_base64 = content['content']
        
        # Decodificar el contenido base64
        file_content = base64.b64decode(file_content_base64)
        
        # Convertir el contenido a un DataFrame de pandas
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Filtrar solo las columnas necesarias si se especificaron
        if columnas_necesarias is not None:
            # Validar que las columnas existen en el DataFrame
            columnas_existentes = [col for col in columnas_necesarias if col in df.columns]
            df_filtrado = df[columnas_existentes]
        else:
            df_filtrado = df  # Si no se especifican columnas, devolver el DataFrame completo
        
        return df_filtrado
    else:
        st.error(f"Error al obtener el archivo desde GitHub. Código de estado: {response.status_code}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si hay un error

def guardar_respuesta_en_csv(nombre, telefono, email, input_text, tipo_opc, mensaje):
    fecha = datetime.datetime.now()
    longitud, latitud, concello_id, ubicacion = concam.procesar_ubicacion(input_text)
    estado="Activo"
    # Generar un ID único para cada respuesta
    respuesta_id = str(uuid.uuid4())
    
    # Limpiar el mensaje de saltos de línea
    mensaje_limpio = mensaje.replace('\n', ' ').replace('\r', ' ')
    
    # Crear una nueva línea de datos para agregar al archivo
    nueva_fila = [respuesta_id, estado, fecha, nombre, telefono, email, latitud, longitud, tipo_opc, mensaje_limpio]
    
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
        filas = [['id', 'estado', 'fecha', 'nombre', 'telefono','email', 'latitud', 'longitud', 'tipo_incidencia', 'comentario']]
    
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

def actualizar_estado(respuesta_id):
    # Cargar los datos del CSV
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Decodificar el contenido base64
        file_info = response.json()
        content = io.StringIO(base64.b64decode(file_info['content']).decode('utf-8'))
        
        # Leer las filas existentes
        reader = csv.reader(content)
        filas = list(reader)
        
        # Buscar la fila con el id correspondiente
        for fila in filas:
            if fila[0] == respuesta_id:  # La primera columna es el ID
                # Cambiar el estado a 'Solucionado'
                fila[1] = 'Solucionado'  # La segunda columna es el estado
                break
        else:
            # Si no se encuentra el id, informar al usuario
            st.error(f"No se encontró el id {respuesta_id} en el archivo.")
            return
        
        # Escribir el contenido CSV actualizado en un buffer de texto
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(filas)
        content_encoded = base64.b64encode(output.getvalue().encode('utf-8')).decode('utf-8')
        
        # Subir el archivo actualizado a GitHub
        data = {
            "message": f"Actualizar estado a Solucionado para ID: {respuesta_id}",
            "content": content_encoded
        }
        if response.status_code == 200:
            data["sha"] = file_info["sha"]  # SHA actual del archivo en GitHub
        
        # Realizar la solicitud de actualización
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print("Estado actualizado exitosamente en GitHub.")
        else:
            print(f"Error al actualizar el archivo en GitHub: {response.status_code} - {response.text}")
    else:
        st.error(f"Error al obtener el archivo desde GitHub. Código de estado: {response.status_code}")


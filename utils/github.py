import base64
import json
import csv
import requests
import streamlit as st
import pandas as pd

# Configuración de GitHub desde los secretos de Streamlit
TOKEN_GITHUB = st.secrets["github"]["token"]
USUARIO_GITHUB = st.secrets["github"]["usuario"]
REPOSITORIO = st.secrets["github"]["repositorio"]
ARCHIVO_GITHUB = st.secrets["github"]["archivo"]

# URL base de la API de GitHub
BASE_URL = f'https://api.github.com/repos/{USUARIO_GITHUB}/{REPOSITORIO}/contents/{ARCHIVO_GITHUB}'

# Función para leer el archivo desde GitHub
def leer_archivo_github():
    headers = {'Authorization': f'token {TOKEN_GITHUB}'}
    response = requests.get(BASE_URL, headers=headers)
    
    if response.status_code == 200:
        # Si el archivo existe, decodificar su contenido desde base64
        archivo = response.json()
        contenido_base64 = archivo['content']
        contenido = base64.b64decode(contenido_base64).decode('utf-8')
        return contenido
    else:
        # Si el archivo no existe, devolver un CSV vacío
        return ''
        
# Función para escribir en el archivo de GitHub
def escribir_en_archivo_github(contenido_nuevo):
    # Leer el contenido actual del archivo
    contenido_actual = leer_archivo_github()
    
    # Agregar el nuevo contenido al final
    contenido_actual += '\n' + contenido_nuevo
    
    # Codificar el contenido a base64 para GitHub
    contenido_base64 = base64.b64encode(contenido_actual.encode('utf-8')).decode('utf-8')
    
    # Obtener el SHA del archivo actual para actualizarlo
    headers = {'Authorization': f'token {TOKEN_GITHUB}'}
    response = requests.get(BASE_URL, headers=headers)
    sha = response.json().get('sha')  # Obtén el SHA del archivo
    
    # Crear el cuerpo del commit
    data = {
        'message': 'Actualización del archivo respuestas.csv',
        'content': contenido_base64,
        'sha': sha,
    }
    
    # Hacer el PUT para actualizar el archivo
    response = requests.put(BASE_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Archivo actualizado correctamente en GitHub.")
    else:
        print(f"Error al actualizar el archivo: {response.status_code}, {response.text}")

# Función que guarda una nueva respuesta en el archivo CSV en GitHub
def guardar_en_archivo(nombre, email, mensaje):
    # Crear una nueva fila CSV
    nueva_fila = f'{nombre},{email},{mensaje}'
    
    # Escribir la respuesta en el archivo GitHub
    escribir_en_archivo_github(nueva_fila)

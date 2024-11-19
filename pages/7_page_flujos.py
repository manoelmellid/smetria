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

import requests
import base64
import csv
import io

# Configuración de GitHub desde los secretos de Streamlit
github_token = st.secrets["github"]["github_token"]
repo = st.secrets["github"]["repo"]
file_path = st.secrets["github"]["file_path"]
url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Obtener el contenido del archivo desde GitHub
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    file_info = response.json()
    
    # Decodificar el contenido base64
    content = io.StringIO(base64.b64decode(file_info['content']).decode('utf-8'))
    
    # Leer el contenido CSV
    reader = csv.reader(content)
    filas = list(reader)
    encabezados = filas[0]
    
    # Definir las columnas a eliminar
    columnas_a_eliminar = ["km", "latitud", "longitud", "tipo_incidencia", "tipo_alerta"]
    
    # Filtrar las columnas que no deben ser eliminadas
    indices_a_eliminar = [encabezados.index(col) for col in columnas_a_eliminar if col in encabezados]
    
    if indices_a_eliminar:
        # Eliminar las columnas correspondientes en cada fila
        for fila in filas:
            for indice in sorted(indices_a_eliminar, reverse=True):  # Ordenar en orden descendente para evitar cambiar índices
                del fila[indice]
        
        # Escribir el contenido CSV actualizado en un buffer de texto
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(filas)
        content_encoded = base64.b64encode(output.getvalue().encode('utf-8')).decode('utf-8')
        
        # Preparar los datos para la solicitud de actualización
        data = {
            "message": "Eliminar columnas 'km', 'latitud', 'longitud', 'tipo_incidencia', 'tipo_alerta' del archivo respuestas2.csv",
            "content": content_encoded,
            "sha": file_info["sha"]  # SHA actual del archivo en GitHub
        }
        
        # Realizar la solicitud de actualización
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print("Archivo actualizado exitosamente en GitHub.")
        else:
            print(f"Error al actualizar el archivo en GitHub: {response.status_code} - {response.text}")
    else:
        print("No se encontraron las columnas especificadas en el archivo.")
else:
    print(f"Error al obtener el archivo desde GitHub. Código de estado: {response.status_code}")




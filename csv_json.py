import json
import csv

def json_to_csv(input_json_file, output_csv_file):
    # Cargar el JSON
    with open(input_json_file) as f:
        data = json.load(f)

    # Abrir el archivo CSV en modo escritura
    with open(output_csv_file, mode='w', newline='') as csvfile:
        # Definir las cabeceras
        fieldnames = ['location_name', 'latitude', 'longitude', 'date_time', 'temperature', 
                      'sky_state', 'precipitation_amount', 'wind_speed', 'wind_direction']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Verificar si 'features' existe y no está vacío
        features = data.get('features', [])
        if not features:
            return  # Salir si no hay features

        # Extraer los datos de interés de cada feature en el JSON
        for feature in features:
            location_name = feature['properties']['name']
            latitude, longitude = feature['geometry']['coordinates']
            
            for day in feature['properties'].get('days', []):
                # Verificar si 'variables' existe y no es None
                if day.get('variables') is None:
                    continue  # Saltar este día si no contiene variables
                
                # Crear un diccionario temporal para almacenar los valores del día
                row_data = {'location_name': location_name, 'latitude': latitude, 'longitude': longitude}
                
                # Agregar cada variable por hora
                variables = {v['name']: v['values'] for v in day['variables']}
                
                # Iterar a través de las horas en los datos de temperatura
                for i in range(len(variables.get('temperature', []))):  # Comprobar si existe 'temperature'
                    row_data['date_time'] = variables['temperature'][i]['timeInstant']
                    row_data['temperature'] = variables['temperature'][i].get('value', 'N/A')
                    row_data['sky_state'] = variables.get('sky_state', [{}])[i].get('value', 'N/A')
                    row_data['precipitation_amount'] = variables.get('precipitation_amount', [{}])[i].get('value', 'N/A')
                    
                    # Si la variable 'wind' está presente, capturamos los datos de velocidad y dirección del viento
                    wind_values = variables.get('wind', [{}])[i]
                    row_data['wind_speed'] = wind_values.get('moduleValue', 'N/A')
                    row_data['wind_direction'] = wind_values.get('directionValue', 'N/A')
                    
                    # Escribir la fila en el archivo CSV
                    writer.writerow(row_data)

import csv

def temperaturas(archivo_csv):
    temperaturas = []

    # Leer el archivo CSV
    with open(archivo_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convertir la temperatura a float y agregar a la lista
            temperaturas.append(float(row['temperature']))

    # Calcular la media, el máximo y el mínimo
    media = sum(temperaturas) / len(temperaturas) if temperaturas else 0
    maximo = max(temperaturas) if temperaturas else None
    minimo = min(temperaturas) if temperaturas else None
    
    return media, maximo, minimo

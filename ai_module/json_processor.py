import json
import re
import requests

URL_DESTINO = 'http://127.0.0.1:8000/tests/api/run-tests/'

def convertir_a_json(texto):
    # Expresión regular para encontrar bloques de JSON en el texto
    json_regex = r'(\{(?:[^{}]|(?:\{[^{}]*\}))*\})'
    match = re.search(json_regex, texto, re.DOTALL)

    if match:
        try:
            # Convierte el texto JSON en un diccionario de Python
            json_data = json.loads(match.group(0))
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
    else:
        print("No se encontró un JSON válido en el texto.")
        return None

def enviar_json(json_data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL_DESTINO, json=json_data, headers=headers)
        
        if response.status_code == 200:
            print("JSON enviado exitosamente.")
            return response.json()
        else:
            print(f"Error al enviar JSON: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error durante el envío del JSON: {e}")
        return None

def procesar_y_enviar_json(texto):
    json_data = convertir_a_json(texto)
    if json_data:
        respuesta = enviar_json(json_data)
        return respuesta
    else:
        print("No se pudo procesar el JSON.")
        return None

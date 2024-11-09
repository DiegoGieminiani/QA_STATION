import json
import requests

URL_DESTINO = 'http://127.0.0.1:8000/tests/api/run-tests/'

def convertir_a_json(texto):
    """
    Convierte un texto a formato JSON. Se espera que el texto sea un JSON en formato string.
    """
    cleaned_text = texto.strip('```json').strip('```').strip()
    try:
        json_data = json.loads(cleaned_text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return None

def enviar_json(json_data):
    """
    Envia datos JSON a la URL destino usando una solicitud POST.
    """
    if not isinstance(json_data, list):
        json_data = [json_data]
    try:
        # No es necesario definir 'Content-Type': 'application/json' porque 'requests' lo hace automáticamente
        response = requests.post(URL_DESTINO, json=json_data)
        
        if response.status_code == 200:
            print("JSON enviado exitosamente.")
            return response.json()  # Esto devuelve la respuesta en formato JSON
        else:
            print(f"Error al enviar JSON: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error durante el envío del JSON: {e}")
        return None

def procesar_y_enviar_json(texto):
    """
    Procesa el texto, lo convierte en JSON y lo envía a la URL destino.
    """
    json_data = convertir_a_json(texto)
    if json_data:
        respuesta = enviar_json(json_data)
        if respuesta:
            return respuesta
        else:
            print("Error al recibir respuesta del servidor.")
            return None
    else:
        print("No se pudo procesar el JSON.")
        return None

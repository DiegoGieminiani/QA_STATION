import os
import re
import requests
from urllib.parse import urlparse
from django.conf import settings
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key =os.getenv('OPENAI_API_KEY')

# Función para extraer la primera URL del texto
def extraer_primera_url(texto):
    url_regex = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"  # Expresión regular para URL
    url_match = re.search(url_regex, texto)
    if url_match:
        return url_match.group(0)
    else:
        return None

# Función para descargar el HTML de la URL
def descargar_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("HTML descargado correctamente.")  # Mensaje de éxito
            return response.text  # Devuelve el contenido HTML
        else:
            print(f"Error al descargar HTML: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error durante la descarga: {str(e)}")
        return None

# Función para extraer el nombre de la página desde la URL
def obtener_nombre_pagina(url):
    parsed_url = urlparse(url)
    nombre_pagina = parsed_url.netloc.replace('.', '_')  # Reemplazar los puntos con guiones bajos
    return nombre_pagina

# Función para guardar el HTML en la carpeta 'media'
def guardar_html(html_content, url):
    try:
        nombre_pagina = obtener_nombre_pagina(url)
        filename = os.path.join(settings.MEDIA_ROOT, f'{nombre_pagina}.html')  # Guardar en la carpeta 'media'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Archivo HTML guardado como {filename}")
        return filename
    except Exception as e:
        print(f"Error al guardar el archivo HTML: {str(e)}")
        return None


# Función principal para procesar la respuesta de ChatGPT y manejar el flujo

def procesar_respuesta_chatgpt(respuesta_chatgpt):
    if respuesta_chatgpt:
        print(f"Respuesta ChatGPT en html_processor antes de procesar: {respuesta_chatgpt}")  # Imprime el valor para confirmar

        # Extrae la primera URL de la respuesta de ChatGPT
        url = extraer_primera_url(respuesta_chatgpt)
        if url:
            print(f"URL extraída: {url}")  # Imprime la URL extraída en la consola

            # Descarga el contenido HTML de la URL
            html_content = descargar_html(url)
            if html_content:
                print("Contenido HTML descargado con éxito.")  # Mensaje de éxito

                # Guarda el HTML en la carpeta media
                html_file = guardar_html(html_content, url)
                if html_file:
                    print(f"Archivo HTML guardado en: {html_file}")  # Imprime el nombre del archivo guardado
                else:
                    print("Error al guardar el archivo HTML.")  # Imprime mensaje de error
            else:
                print("Error al descargar el HTML.")  # Imprime mensaje de error
        else:
            print("No se encontró una URL válida en la respuesta.")  # Imprime mensaje de error
    else:
        print("No se generó ninguna respuesta de ChatGPT en html_processor.")  # Imprime mensaje de error




# Función para procesar el HTML y generar el JSON basado en la respuesta de ChatGPT
def procesar_html(respuesta_chatgpt):
    # Pedir el texto (Prompt)
    texto_prompt = "Identifica todos los elementos HTML con los que el usuario debe interactuar y correspondientes a los casos de prueba."

    # Obtener la lista de archivos en la carpeta media
    html_folder = settings.MEDIA_ROOT
    archivos_html = os.listdir(html_folder)

    if archivos_html:
        # Ordenar los archivos por fecha de modificación (el más reciente primero)
        archivos_html.sort(key=lambda x: os.path.getmtime(os.path.join(html_folder, x)), reverse=True)
        
        # Obtener el último archivo
        ultimo_archivo = archivos_html[0]
        ruta_ultimo_archivo = os.path.join(html_folder, ultimo_archivo)

        # Leer el contenido del archivo HTML
        with open(ruta_ultimo_archivo, 'r', encoding='utf-8') as file:
            contenido_html = file.read()

        # Concatenar el contenido del HTML al prompt
        prompt = texto_prompt + "\n\n" + contenido_html
    else:
        return "No hay archivos HTML en la carpeta para procesar."

    mensaje = [
        {"role": "system", "content": "Eres un asistente experto en automatización de pruebas de software cuya tarea es analizar el HTML proporcionado y generar un JSON de casos de prueba compatible con Selenium."},
        {"role": "system", "content": """
    Tu objetivo es identificar todos los elementos HTML interactivos relevantes en el archivo HTML y crear casos de prueba en formato JSON. Cada caso de prueba debe estar separado y debe incluir los siguientes campos obligatorios:
    - **url**: La URL de la página que se está probando.
    - **actions**: Una lista de acciones que deben realizarse en este caso de prueba.

    Para cada acción dentro del caso de prueba, usa los siguientes campos:
    - **action**: La acción que el usuario debe realizar (por ejemplo, "click", "enter_data", "submit").
    - **element_type**: El tipo de selector de elemento que debe usarse en Selenium. Los valores permitidos son: id, name, xpath, css_selector, class_name, tag_name, link_text, partial_link.
    - **value**: El valor del selector para el elemento (por ejemplo, el id o el xpath del elemento).
    - **input_value** (opcional): En caso de ser necesario, el valor que se debe ingresar en el campo (solo para acciones de entrada de datos como "enter_data").
        """},
        {"role": "system", "content": """
    Aquí tienes un ejemplo del formato JSON esperado para los casos de prueba:
    [
        {
            "url": "https://www.tu-url-aqui.com",
            "actions": [
                {
                    "action": "click",
                    "element_type": "id",
                    "value": "login2"
                },
                {
                    "action": "enter_data",
                    "element_type": "name",
                    "value": "q", 
                    "input_value": "Texto a ingresar" 
                },
                {
                    "action": "submit",
                    "element_type": "xpath",
                    "value": "//button[@type='submit']"
                }
            ]
        },
        {
            "url": "https://www.otro-url-aqui.com",
            "actions": [
                {
                    "action": "click",
                    "element_type": "css_selector",
                    "value": ".btn-primary"
                },
                {
                    "action": "enter_data",
                    "element_type": "id",
                    "value": "email",
                    "input_value": "usuario@example.com"
                },
                {
                    "action": "enter_data",
                    "element_type": "id",
                    "value": "password",
                    "input_value": "contraseñaSegura"
                },
                {
                    "action": "submit",
                    "element_type": "name",
                    "value": "login"
                }
            ]
        }
    ]
        """},
        {"role": "system", "content": """
    Asegúrate de que:
    1. Cada caso de prueba esté claramente separado en su propio objeto JSON dentro de una lista.
    2. Cada caso de prueba tenga todos los campos requeridos: "url" y "actions".
    3. Las acciones dentro de cada caso de prueba estén bien detalladas y estructuradas con los campos correctos.

    Entrega exclusivamente el JSON en el formato mostrado, sin explicaciones adicionales ni texto adicional fuera del JSON.
        """},
        {"role": "assistant", "content": "La respuesta generada debe ser exclusivamente un JSON con los casos de prueba en el formato solicitado, sin explicaciones adicionales."},
        {"role": "assistant", "content": respuesta_chatgpt},  
        {"role": "user", "content": "Identifica todos los elementos HTML interactivos y genera el JSON para los casos de prueba basados en estos elementos, siguiendo estrictamente el formato indicado."}
    ]

    # Realizar la solicitud a OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensaje,
        temperature=0.1
    )

    # Obtener la respuesta de OpenAI
    respuesta = response.choices[0].message.content
    print("Este es el mensaje que entrega la respuesta combinada de casos de prueba:          ",respuesta)
    return respuesta


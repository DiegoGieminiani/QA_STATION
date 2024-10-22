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

    # Crear el mensaje para OpenAI, usando respuesta_chatgpt en lugar de historial
    mensaje = [
        {"role": "system", "content": "Analiza el archivo HTML adjunto y entrega un JSON en este formato para cada caso de prueba"},
        {"role": "system", "content": "Este JSON se le pasara a Selenium , por lo que el element_type debe ser uno de estos valores: id, name, xpath, css_selector, class_name, tag_name, link_text, partial_link"},
        {"role": "system", "content": """
         {
  "url": "https://www.tu-url-aqui.com",
  "actions": [
    {
      "action": "enter_data",
      "element_type": "name",
      "value": "q",
      "input_value": "Texto a ingresar"
    }
  ]
}

Asegúrate de sustituir los valores correspondientes según el contenido del documento y el HTML proporcionado.
         """},
        {"role": "assistant", "content": respuesta_chatgpt},  # Cambiado a usar respuesta_chatgpt
        {"role": "user", "content": prompt}
    ]

    print("ESTA ES LA RESPUESTA_CHATGPT QUE LE PASAMOS:", respuesta_chatgpt)
    
    # Realizar la solicitud a OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensaje,
        temperature=0.1,
        max_tokens=2500
    )

    # Obtener la respuesta de OpenAI
    respuesta = response.choices[0].message.content
    print("Este es el mensaje que entrega la respuesta combinada de casos de prueba:          ",respuesta)
    return respuesta




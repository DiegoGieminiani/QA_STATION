import os
import PyPDF2
import openai
from dotenv import load_dotenv
from django.conf import settings
from .html_processor import procesar_respuesta_chatgpt
from .models import TestCase


#Cargar variable de entorno
load_dotenv()
openai.api_key=os.getenv('OPENAI_API_KEY')


# Definir la carpeta de subida como se indica en settings.py
UPLOAD_FOLDER = settings.MEDIA_ROOT

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

HISTORIAL_BASE = [
    {"role": "system", "content": "Eres un asistente experto en calidad de software cuya tarea es generar solo casos de prueba detallados y estructurados para aplicaciones web."},
    {"role": "system", "content": """
Tu objetivo es crear una lista de casos de prueba en texto plano para la aplicación web Demoblaze. Los casos de prueba deben estar en un formato claro y específico, 
adecuado para pruebas manuales y automatización. No incluyas encabezados, introducciones, tablas de contenido, secciones adicionales, conclusiones ni ningún tipo de formato o estructura de documento. Devuelve exclusivamente los casos de prueba en el formato de texto plano especificado.
    """},
    {"role": "system", "content": """
Para cada caso de prueba, utiliza el siguiente formato en texto plano y simple, sin incluir encabezados, tablas de contenido, listas numeradas o cualquier formato visual complejo:

URL: [URL de la página que se está probando]
ID: [Identificador único del caso de prueba, como TC001]
NOMBRE: [Un nombre descriptivo que indique el propósito del caso de prueba]
PASO A PASO: 
- Paso 1: [Descripción detallada de la acción]
- Paso 2: [Descripción detallada de la siguiente acción]
- etc.
RESULTADO ESPERADO: [Descripción del resultado esperado tras completar los pasos]

Ejemplo de un caso de prueba:
URL: https://example.com/login
ID: TC001
NOMBRE: Verificar inicio de sesión exitoso
PASO A PASO:
- Navegar a la URL de inicio de sesión.
- Ingresar un nombre de usuario válido en el campo "username".
- Ingresar una contraseña válida en el campo "password".
- Hacer clic en el botón "Iniciar sesión".
RESULTADO ESPERADO: El usuario es redirigido a su panel de control y se muestra el mensaje "Inicio de sesión exitoso".
    """},
    {"role": "system", "content": """
Por favor, genera casos de prueba que cubran lo siguiente:
- Flujos de usuario críticos, como inicio de sesión, registro y recuperación de contraseña.
- Validación de formularios (incluyendo datos válidos e inválidos).
- Interacción con elementos interactivos como menús desplegables, botones de acción y campos de entrada.
- Escenarios alternativos o errores comunes, como intentos de inicio de sesión fallidos o envíos de formularios incompletos.
    """},
    {"role": "system", "content": """
Asegúrate de que cada caso de prueba esté claramente separado y siga el formato indicado en texto plano. No incluyas ninguna información adicional como encabezados, introducciones o conclusiones. Solo entrega los casos de prueba en el formato solicitado.
    """}
]



def process_chat_request(request):
    # Inicializa un historial vacío si no existe
    historial = []

    # Verifica si el archivo está en la solicitud
    if 'archivo' in request.FILES:
        archivo = request.FILES['archivo']

        if archivo and allowed_file(archivo.name):
            # Guarda el archivo PDF
            filepath = os.path.join(UPLOAD_FOLDER, archivo.name)

            with open(filepath, 'wb+') as f:
                for chunk in archivo.chunks():
                    f.write(chunk)

            # Lee el contenido del PDF
            with open(filepath, 'rb') as f:
                lector_pdf = PyPDF2.PdfReader(f)
                texto_pdf = ''
                for pagina in range(len(lector_pdf.pages)):
                    texto_pdf += lector_pdf.pages[pagina].extract_text()

            # Añade el contenido del PDF al historial
            historial.append({"role": "assistant", "content": f"Este es el contenido del archivo PDF:\n{texto_pdf}"})

    mensaje_usuario = request.POST.get('mensaje')

    if mensaje_usuario:
        historial.append({"role": "user", "content": f"Genera el documento de casos de prueba en base a esta URL:\n{mensaje_usuario}, la cual debe ir en el documento generado"})

        try:
            # Envía la conversación a la API de OpenAI
            completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=historial
            )

            # Obtiene la respuesta de ChatGPT
            respuesta_chatgpt = completion.choices[0].message.content

            # Imprime la respuesta para verificar
            print(f"Respuesta obtenida: {respuesta_chatgpt}")

            # Llama a la función para procesar la respuesta
            procesar_respuesta_chatgpt(respuesta_chatgpt)

            # Devuelve solo la respuesta sin agregarla al historial
            return respuesta_chatgpt
        except Exception as e:
            print(f"Error al llamar a OpenAI: {str(e)}")
            return None
        
    return None



def guardar_en_bd(respuesta_chatgpt, mensaje_usuario):
    """
    Guarda las variables respuesta_chatgpt y mensaje_usuario en la base de datos.
    """
    try:
        # Crea una nueva instancia de TestCase y asigna los valores
        nuevo_test_case = TestCase(
            actions_data=respuesta_chatgpt,
            name=mensaje_usuario
        )
        
        # Guarda la instancia en la base de datos
        nuevo_test_case.save()
        
        print("Datos guardados correctamente en la base de datos.")
        return True
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return False
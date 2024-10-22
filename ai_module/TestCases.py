import os
import PyPDF2
import openai
from dotenv import load_dotenv
from django.conf import settings
from .html_processor import procesar_respuesta_chatgpt


#Cargar variable de entorno
load_dotenv()
openai.api_key =os.getenv('OPENAI_API_KEY')


# Definir la carpeta de subida como se indica en settings.py
UPLOAD_FOLDER = settings.MEDIA_ROOT

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

historial = [
    {"role": "system", "content": "Eres un asistente que ayuda a crear casos de prueba"},
    {"role": "system", "content": "El titulo del deocumento debe ser profesional y debe contener el nombre de la pagina y obligatoriamente la Url"},
    {"role": "system", "content": "Los casos de prueba deben contener: ID, Nombre, Paso a Paso y  Respuesta Esperada"}
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
        historial.append({"role": "user", "content": f"Genera el documento de casos de prueba en base a esta URL:\n{mensaje_usuario}"})

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



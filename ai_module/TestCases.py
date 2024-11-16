import os
import PyPDF2
import openai
from dotenv import load_dotenv
from django.conf import settings
from .html_processor import procesar_respuesta_chatgpt
from .models import TestCase
from user_projects.models import Project


#Cargar variable de entorno
load_dotenv()
openai.api_key=os.getenv('OPENAI_API_KEY')


# Definir la carpeta de subida como se indica en settings.py
UPLOAD_FOLDER = settings.MEDIA_ROOT

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

historial = [
    {"role": "system", "content": "Eres un asistente experto en calidad de software cuya tarea es generar solo casos de prueba detallados y estructurados para aplicaciones web."},
    {"role": "system", "content": """
Limitate a solo generar casos de prueba, no generes conclusiones ni recomendaciones
    """},
    {"role": "system", "content": """
Los casos de prueba deben contener solo estos puntos: URL, ID, NOMBRE, PASO A PASO, RESULTADO ESPERADO
    """},
    {"role": "system", "content": """
Los casos de prueba deben abarcar estos temas:
- Flujos de usuario críticos, como inicio de sesión y registro
- Validación de formularios (incluyendo datos válidos e inválidos).
- Interacción con elementos interactivos como menús desplegables, botones de acción y campos de entrada.
- Escenarios alternativos o errores comunes, como intentos de inicio de sesión fallidos o envíos de formularios incompletos.
    """},
    {"role": "system", "content": """
Asegúrate de que cada caso de prueba esté claramente separado y siga el formato indicado. No incluyas ninguna información adicional.
    """},
    {"role": "system", "content": "Ten en cuenta que siempre para iniciar sesion, hay que registrarse primero"}

]



def process_chat_request(request):
    # Inicializa un historial vacío si no existe
    global historial

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
                model="gpt-4o",
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


def guardar_en_bd(respuesta_chatgpt, mensaje_usuario, proyecto_id):
    """
    Guarda las variables respuesta_chatgpt y mensaje_usuario en la base de datos
    asociadas al proyecto específico identificado por proyecto_id.
    """
    try:
        # Obtener el proyecto específico por su ID
        proyecto = Project.objects.filter(id=proyecto_id).first()
        
        if not proyecto:
            print("No se encontró un proyecto con el ID proporcionado.")
            return False
        
        # Crear una nueva instancia de TestCase y asignar los valores
        nuevo_test_case = TestCase(
            actions_data=respuesta_chatgpt,
            name=mensaje_usuario,
            project=proyecto  # Asociar el proyecto específico
        )
        
        # Guardar la instancia en la base de datos
        nuevo_test_case.save()
        
        print("Caso de prueba guardado correctamente en la base de datos asociado al proyecto.")
        return True
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return False
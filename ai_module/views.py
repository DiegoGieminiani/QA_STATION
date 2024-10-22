from django.shortcuts import render
from .TestCases import process_chat_request
from .html_processor import procesar_respuesta_chatgpt, procesar_html

def test_cases_view(request):
    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente
            
        return render(request, 'testcases.html', {'respuesta': respuesta_chatgpt})
    
    # Si la solicitud es GET, renderizar un formulario vacío
    return render(request, 'testcases.html')


def ejecutar_html_processor(request):
    # Asegúrate de inicializar 'respuesta' y 'resultado' fuera de la verificación de POST
    respuesta_chatgpt = None
    resultado_procesado = None
    
    if request.method == 'POST':
        # Simula o toma la respuesta generada por ChatGPT anteriormente
        respuesta_chatgpt = request.POST.get('respuesta', 'No hay respuesta disponible aún.')

        # Llama a procesar_html() para procesar el HTML
        resultado_procesado = procesar_html(respuesta_chatgpt)

        # Devuelve un mensaje indicando que se ha ejecutado el proceso
        return render(request, 'testcases.html', {
            'mensaje': 'Se ha ejecutado todo el proceso.',
            'respuesta': respuesta_chatgpt,  # Muestra la respuesta generada
            'resultado': resultado_procesado  # Muestra el resultado del procesamiento HTML
        })
    
    # Si no es POST, asegúrate de devolver el contenido previo
    return render(request, 'testcases.html', {
        'respuesta': respuesta_chatgpt,  # Muestra la respuesta previa
        'mensaje': 'No se ha ejecutado aún el proceso.'
    })
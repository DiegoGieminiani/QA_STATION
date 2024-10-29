from django.shortcuts import render
import markdown2
from django.http import JsonResponse
from .TestCases import process_chat_request
from .html_processor import procesar_respuesta_chatgpt, procesar_html
from .json_processor import procesar_y_enviar_json
import json

def test_cases_view(request):
    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente

            # Convertir Markdown a HTML
            respuesta_html = markdown2.markdown(respuesta_chatgpt)

        return render(request, 'testcases.html', {'respuesta': respuesta_html})  # Enviar HTML convertido
    
    # Si la solicitud es GET, renderizar un formulario vacío
    return render(request, 'testcases.html')

def ejecutar_html_processor(request):
    respuesta_chatgpt = None
    resultado_procesado = None
    
    if request.method == 'POST':
        respuesta_chatgpt = request.POST.get('respuesta', 'No hay respuesta disponible aún.')
        
        # Llama a procesar_html() y guarda el resultado en una variable
        resultado_procesado = procesar_html(respuesta_chatgpt)
        
        # Renderiza la respuesta y el resultado en la plantilla
        return render(request, 'testcases.html', {
            'mensaje': 'Se ha ejecutado todo el proceso.',
            'respuesta': respuesta_chatgpt,
            'resultado_procesado': resultado_procesado  # Incluye el resultado en el HTML
        })
    
    return render(request, 'testcases.html', {
        'mensaje': 'No se ha ejecutado aún el proceso.'
    })

def enviar_json_view(request):
    if request.method == 'POST':
        # Lee el JSON enviado desde el frontend
        data = json.loads(request.body)
        resultado_procesado = data.get('resultado_procesado', '')

        # Procesa y envía el JSON
        resultado = procesar_y_enviar_json(resultado_procesado)
        if resultado:
            mensaje = "JSON enviado exitosamente."
        else:
            mensaje = "Error al enviar el JSON."

        return JsonResponse({'mensaje': mensaje})
    
    return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)



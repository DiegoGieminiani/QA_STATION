from django.shortcuts import render, get_object_or_404, redirect 
import markdown2
from django.http import JsonResponse
from .TestCases import process_chat_request, guardar_en_bd
from .html_processor import procesar_respuesta_chatgpt, procesar_html
from .json_processor import procesar_y_enviar_json
from user_projects.models import Project
from .forms import TestCaseForm
import json



def test_cases_view(request):
    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente

            # Convertir Markdown a HTML
            respuesta_html = markdown2.markdown(respuesta_chatgpt)

        return render(request, 'ai_module/testcases.html', {'respuesta': respuesta_html})  # Enviar HTML convertido
    
    # Si la solicitud es GET, renderizar un formulario vacío
    return render(request, 'ai_module/testcases.html')

def ejecutar_html_processor(request):
    respuesta_chatgpt = None
    resultado_procesado = None
    
    if request.method == 'POST':
        respuesta_chatgpt = request.POST.get('respuesta', 'No hay respuesta disponible aún.')
        
        # Llama a procesar_html() y guarda el resultado en una variable
        resultado_procesado = procesar_html(respuesta_chatgpt)

        # Devuelve un mensaje indicando que se ha ejecutado el proceso
        return render(request, 'ai_module/testcases.html', {
            'mensaje': 'Se ha ejecutado todo el proceso.',
            'respuesta': respuesta_chatgpt,
            'resultado_procesado': resultado_procesado  # Incluye el resultado en el HTML
        })
    
    # Si no es POST, asegúrate de devolver el contenido previo
    return render(request, 'ai_module/testcases.html', {
        'respuesta': respuesta_chatgpt,  # Muestra la respuesta previa
        'mensaje': 'No se ha ejecutado aún el proceso.'
    })

def enviar_json_view(request):
    if request.method == 'POST':
        # Lee el JSON enviado desde el frontend
        print(request.body)
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


def add_test_case(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.project = project  # Asigna el TestCase al Project
            test_case.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TestCaseForm()
    return render(request, 'add_test_case.html', {'form': form, 'project': project})



def test_cases_view(request):
    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente

            # Convertir Markdown a HTML
            respuesta_html = markdown2.markdown(respuesta_chatgpt)

            # Obtén el mensaje del usuario de la solicitud
            mensaje_usuario = request.POST.get('mensaje', '')

            # Llama a la nueva función para guardar en la base de datos
            guardar_en_bd(respuesta_chatgpt, mensaje_usuario)

        return render(request, 'ai_module/testcases.html', {'respuesta': respuesta_html})  # Enviar HTML convertido
    
    # Si la solicitud es GET, renderizar un formulario vacío
    return render(request, 'ai_module/testcases.html')

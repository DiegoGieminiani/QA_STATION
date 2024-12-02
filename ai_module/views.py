from django.shortcuts import render, get_object_or_404, redirect 
import markdown2
from django.http import JsonResponse
from django.http import HttpResponse
from .TestCases import process_chat_request, guardar_en_bd
from .html_processor import procesar_respuesta_chatgpt, procesar_html
from .json_processor import procesar_y_enviar_json, guardar_functional_test
from user_projects.models import Project
from .forms import TestCaseForm
import json
from .models import TestCase

def view_cases(request, project_id):
    print('\n'*10)
    mensajes = TestCase.objects.filter(project_id = project_id)
    
    for mensaje in mensajes:
        print('mensaje')
        msg = mensaje.actions_data.replace('\n', '<br>')
        msg+= '\n'

  
    # Si no es POST, asegúrate de devolver el contenido previo
    return render(request, 'ai_module/testcases.html', {
        'respuesta': msg,  # Muestra la respuesta previa
        'mensaje': [mensaje.actions_data for mensaje in mensajes],
        'project_id': project_id  # Incluye project_id en todas las respuestas
    })

def ejecutar_html_processor(request, project_id):
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
            'resultado_procesado': resultado_procesado,  # Incluye el resultado en el HTML
            'project_id': project_id  # Asegúrate de incluir project_id
        })
    
    mensaje = TestCase.objects.filter(project_id = project_id)
    # Si no es POST, asegúrate de devolver el contenido previo
    return render(request, 'ai_module/testcases.html', {
        'respuesta': mensaje.actions_data,  # Muestra la respuesta previa
        'mensaje': mensaje.actions_data,
        'project_id': project_id  # Incluye project_id en todas las respuestas
    })


def enviar_json_view(request, project_id):
    if request.method == 'POST':
        try:
            # Lee el JSON enviado desde el frontend
            print(request.body)
            data = json.loads(request.body)
            resultado_procesado = data.get('resultado_procesado', '')

            # Procesa y envía el JSON (lógica proporcionada previamente)
            resultado = procesar_y_enviar_json(resultado_procesado)
            
            # Determina el mensaje según el resultado del envío
            if resultado:
                mensaje = "JSON enviado exitosamente."
                
                # Guardar en la base de datos
                json_data = resultado_procesado  # Asegúrate de que este sea el JSON correcto
                origen = "Automatico"  # Origen identificativo
                proyecto_id = get_object_or_404(Project, id=project_id, user=request.user)  # Debes enviar esto en el JSON
                test_case_id = data.get('test_case_id')  # Debes enviar esto en el JSON

                if not proyecto_id or not test_case_id:
                    return JsonResponse({
                        'mensaje': "Faltan los IDs de proyecto o caso de prueba para guardar en la base de datos."
                    }, status=400)

                guardado_exitoso = guardar_functional_test(json_data, origen, proyecto_id, test_case_id)
                
                if guardado_exitoso:
                    mensaje += " Datos guardados exitosamente en la base de datos."
                else:
                    mensaje += " Error al guardar los datos en la base de datos."

            else:
                mensaje = "Error al enviar el JSON."

            return JsonResponse({'mensaje': mensaje})

        except json.JSONDecodeError:
            return JsonResponse({'mensaje': "Error al decodificar el JSON enviado."}, status=400)
        except Exception as e:
            return JsonResponse({'mensaje': f"Error inesperado: {e}"}, status=500)

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


def test_cases_view(request, project_id):
    # Obtiene el proyecto utilizando `project_id` y verifica que pertenece al usuario autenticado
    proyecto = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente

            # Convierte Markdown a HTML
            respuesta_html = markdown2.markdown(respuesta_chatgpt)

            # Obtiene el mensaje del usuario de la solicitud
            mensaje_usuario = request.POST.get('mensaje', '')

            # Guarda el caso de prueba en la base de datos asociado al proyecto
            guardar_en_bd(respuesta_chatgpt, mensaje_usuario, proyecto.id)

        # Renderiza la respuesta HTML si `respuesta_chatgpt` está vacía o hubo algún error
        return render(request, 'ai_module/testcases.html', {'respuesta': respuesta_html, 'project_id': project_id})

    # Si la solicitud es GET, renderiza el formulario de creación de casos de prueba con el proyecto seleccionado
    return render(request, 'ai_module/testcases.html', {'proyecto': proyecto, 'project_id': project_id})




from .models import TestCase, StepByStep, Project
from django.shortcuts import render, get_object_or_404, redirect 
import markdown2
from django.http import JsonResponse
from django.http import HttpResponse
from .TestCases import process_chat_request
from .html_processor import procesar_respuesta_chatgpt, procesar_html
from .json_processor import procesar_y_enviar_json, guardar_functional_test
from user_projects.models import Project
from .forms import TestCaseForm
import json
from .models import TestCase, StepByStep, FunctionalTest, Action




#FUNCION PARA GENERAR LOS CASOS DE PRUEBA (LENGUAJE NATURAL) Y GUARDAR EN LA BASE DE DATOS
def test_cases_view(request, project_id):
    # Obtiene el proyecto asociado al usuario autenticado
    proyecto = get_object_or_404(Project, id=project_id, user=request.user)
    validate_data={}
    test_cases_list=[]
    

    if request.method == 'POST':
        # Procesa el archivo y genera la respuesta desde TestCases.py
        respuesta_chatgpt = process_chat_request(request)  # Genera los casos de prueba y almacena la respuesta
        
        if respuesta_chatgpt:  # Verifica si la respuesta existe
            procesar_respuesta_chatgpt(respuesta_chatgpt)  # Pasa la respuesta de ChatGPT directamente

            # Convierte Markdown a HTML
            respuesta_html = markdown2.markdown(respuesta_chatgpt)

            # Guarda el caso de prueba en la base de datos asociado al proyecto
            #guardar_en_bd(respuesta_chatgpt, mensaje_usuario, proyecto.id)
            proyecto = Project.objects.filter(id=project_id).first()
            json_strip=respuesta_chatgpt.strip('```json').strip('```').strip()
            # print(respuesta_chatgpt)
            # print(json_strip)
            json_data=json.loads(json_strip)

            for testcase in json_data:
                case_data={
                    'testcase':None, 
                    'pasos':[]
                }

                use_id = testcase["ID"]
                nombre = testcase["NOMBRE"]
                url = testcase["URL"]
                resultado_esperado = testcase["RESULTADO ESPERADO"]
                new_testcase = TestCase(
                    use_id = use_id,
                    nombre = nombre,
                    url = url,
                    resultado_esperado = resultado_esperado
                )
                new_testcase.save()
                case_data['testcase']=new_testcase
                # print("✔️🟩"*50)
                stepbystep_list=[]
                for step in testcase["PASO A PASO"]:
                    pasos = step
                    test_case = new_testcase.test_case_id
                    new_step =StepByStep(
                        pasos = pasos,
                        test_case = new_testcase
                    )
                    
                    new_step.save()
                    stepbystep_list.append(new_step)
                case_data['pasos']=stepbystep_list
                test_cases_list.append(case_data)

                    # print("✔️🟩"*50)
        # Renderiza el template con la respuesta y los casos de prueba guardados
            # Renderiza la respuesta HTML si respuesta_chatgpt está vacía o hubo algún error
    return render(
        request, 
        'ai_module/testcases.html', {
            'project_id': project_id,
            'casos_prueba': test_cases_list, 
        }
    )



#AQUI SE GENERA EL JSON DE HTML_PROCESSOR
def ejecutar_html_processor(request, project_id):
    respuesta_chatgpt = None
    resultado_procesado = None

    if request.method == 'POST':
        respuesta_chatgpt = request.POST.get('respuesta')
        proyecto = get_object_or_404(Project, id=project_id, user=request.user)
        print("✅*20")
        print("RESPUESTA GPT 1")
        print (respuesta_chatgpt)
        print("✅*20")
        
        # Llama a procesar_html() y guarda el resultado en una variable
        resultado_procesado = procesar_html(respuesta_chatgpt)
        print("RESPUESTA PROCESAR HTML")

        print (resultado_procesado)
        print("✅*20")

        respuesta_chatgpt = resultado_procesado.strip('```json').strip('```').strip()
        print("RESPUESTA STRIPEAO")

        print (respuesta_chatgpt)
        print("✅*20")
        respuesta_chatgpt = json.loads(respuesta_chatgpt)
        print("RESPUESTA JSON")

        print (respuesta_chatgpt)
        print("✅*20")
        for data in respuesta_chatgpt:
            print("DATA\n\n\n\n\n\n\n")

            print(data)
            print("✅*20")
            url = data["url"]
            new_FunctionalTest = FunctionalTest(
                url = url,
                project = proyecto
            )
            new_FunctionalTest.save()
            # print("Se guardo en Functional Test 👌"*52)
            for _action in data["actions"]:
                try:
                    action = _action["action"]
                except:
                    action = ""
                try:
                    element_type = _action["element_type"]
                except:
                    element_type = ""
                try:
                    value = _action["value"]
                except:
                    value = ""
                try:
                    input_value= _action["input_value"]
                except:
                    input_value= ""
                # print("✔️🟩"*50)
                new_Action = Action(
                    action = action,
                    element_type = element_type,
                    value = value,
                    input_value = input_value,
                    functional_test = new_FunctionalTest,
                    #Pendiente para ver 
                    paso_id = None
                ).save()
                # print("Se guardo en Action Correctamente")

        # Devuelve un mensaje indicando que se ha ejecutado el proceso
        return render(request, 'ai_module/testcases.html', {
            'mensaje': 'Se ha ejecutado todo el proceso.',
            'respuesta': resultado_procesado,
            'resultado_procesado': resultado_procesado,  # Incluye el resultado en el HTML
            'project_id': project_id,  # Asegúrate de incluir project_id
            'flag' : True 
        })

    
    # Si no es POST, asegúrate de devolver el contenido previo
    return render(request, 'ai_module/testcases.html',{
            'mensaje': 'Se ha ejecutado todo el proceso.',
            'respuesta': resultado_procesado,
            'resultado_procesado': resultado_procesado,  # Incluye el resultado en el HTML
            'project_id': project_id,  # Asegúrate de incluir project_id
            'flag' : True 
        })



#FUNCION PARA ENVIAR EL JSON A LA RAMA DE DIEGUITO
def enviar_json_view(request, project_id):
    
    if request.method == 'POST':
        try:
            # Lee el JSON enviado desde el frontend
            print("Imprime el request----------------------------------------------------------------------------------")
            print(request)
            data = json.loads(request.body)
            resultado_procesado = data.get('resultado_procesado', '')

            # Procesa y envía el JSON (lógica proporcionada previamente)
            json_procesado = procesar_y_enviar_json(resultado_procesado)
            # print(data)
            # Determina el mensaje según el resultado del envío
            if json_procesado:
                mensaje = "JSON enviado exitosamente."
                
            else:
                mensaje = "Error al enviar el JSON."

            return JsonResponse({'mensaje': mensaje})

        except json.JSONDecodeError:
            return JsonResponse({'mensaje': "Error al decodificar el JSON enviado."}, status=400)
        except Exception as e:
            return JsonResponse({'mensaje': f"Error inesperado: {e}"}, status=500)

    return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)



#NO SE QUE ES LO QUE HACE ESTA WEA
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
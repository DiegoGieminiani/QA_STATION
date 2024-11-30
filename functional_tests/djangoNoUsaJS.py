from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from urllib.parse import urlparse

def isValidUrl(string):
    try:
        urlparse(string).netloc
        return True
    except:
        return False
    


@require_POST
def validate_and_collect_actions(request):
    actions = []
    actions_without_element_type_value = ['accept_alert', 'confirm_alert', 'prompt_alert']
    
    action_rows = request.POST.getlist('action[]')
    element_types = request.POST.getlist('element_type[]')
    values = request.POST.getlist('value[]')
    input_values = request.POST.getlist('input_value[]')
    
    for i in range(len(action_rows)):
        action = action_rows[i]
        element_type = element_types[i]
        value = values[i]
        
        # Validación de campos
        if action not in actions_without_element_type_value and (not element_type or not value):
            return JsonResponse({
                'success': False,
                'message': "Por favor, asegúrate de que todos los campos estén llenos."
            })
        
        action_data = {'action': action}
        
        if action not in actions_without_element_type_value:
            action_data['element_type'] = element_type
            action_data['value'] = value
        
        if action in ['enter_data', 'select']:
            action_data['input_value'] = input_values[i] if input_values[i] else None
        
        if action.startswith('verify_'):
            action_data['expected_value'] = input_values[i] if input_values[i] else None
        
        actions.append(action_data)
    
    # Aquí puedes procesar las acciones como necesites
    return JsonResponse({
        'success': True,
        'actions': actions
    })


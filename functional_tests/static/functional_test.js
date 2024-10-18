let executionCount = 0;  // Contador de ejecuciones

// Mapeo de categorías a sus respectivas acciones
const actionCategories = {
    'navigation': ['click', 'scroll_to_element', 'switch_tab', 'back', 'forward', 'navigate_to_url', 'refresh'],
    'forms': ['enter_data', 'select', 'check_checkbox', 'clear_field', 'select_radio_button', 'submit_form'],
    'alerts': ['accept_alert', 'confirm_alert', 'prompt_alert', 'enter_prompt', 'alert_is_present', 'dismiss_alert'],
    'keyboard_mouse': ['send_keys', 'drag_and_drop', 'context_click', 'double_click', 'click_and_hold', 'hover', 'release', 'scroll'],
    'javascript': ['execute_script', 'change_element_style', 'get_element_property', 'scroll_into_element'],
    'data_extraction': ['extract_text', 'extract_attribute', 'extract_dropdown_options', 'extract_links', 'extract_list_items', 'extract_table_data'],
    'verifications': ['verify_text', 'verify_url', 'verify_attribute_value', 'verify_element_has_child', 'verify_element_presence', 'verify_element_selected']
};

// Manejador de evento para enviar el formulario
document.getElementById('testForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar el envío predeterminado del formulario

    executionCount += 1;  // Aumentar el contador global

    const url = document.getElementById('url').value;
    const logContainer = document.getElementById('log-output');
    logContainer.innerHTML = '';  // Limpiar logs anteriores

    // Aquí debes construir las acciones que quieres enviar al servidor
    const actions = [];
    let formIsValid = true;

    // Recorre todas las filas de acción y agrega las acciones al array 'actions'
    document.querySelectorAll('#actionContainer .action-row').forEach((row) => {
        const action = row.querySelector('select[name="action[]"]').value;
        const element_type = row.querySelector('input[name="element_type[]"]').value;
        const value = row.querySelector('input[name="value[]"]').value;

        // Verificar si la acción es diferente a las que no necesitan 'element_type' ni 'value'
        const actionsWithoutElementTypeValue = ['accept_alert', 'confirm_alert', 'prompt_alert'];
        if (!actionsWithoutElementTypeValue.includes(action) && (!element_type || !value)) {
            alert("Por favor, asegúrate de que todos los campos estén llenos.");
            formIsValid = false;
            return;  // Salir de la función si falta algún campo obligatorio
        }

        let actionData = { action };

        // Añadir 'element_type' y 'value' si no es una acción que las omite
        if (!actionsWithoutElementTypeValue.includes(action)) {
            actionData.element_type = element_type;
            actionData.value = value;
        }

        // Si la acción es "enter_data" o "select", se usa "input_value"
        if (action === 'enter_data' || action === 'select') {
            const input_value = row.querySelector('input[name="input_value[]"]').value || null;
            actionData.input_value = input_value;
        }

        // Si la acción es "verify_text" u otra verificación, se usa "expected_value"
        if (action.startsWith('verify_')) {
            const expected_value = row.querySelector('input[name="input_value[]"]').value || null;
            actionData.expected_value = expected_value;
        }

        actions.push(actionData);
    });

    if (!formIsValid) return;

    // Crear los datos que vamos a enviar
    const data = {
        url: url,
        actions: actions
    };

    console.log("Datos enviados al servidor:", data);  // Verifica que los datos se están preparando correctamente

    // Enviar los datos al servidor con fetch
    fetch('/tests/run/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value  // Incluye el token CSRF
        },
        body: JSON.stringify(data)  // Convertir los datos a JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos procesados:", data);  // Muestra los datos recibidos del servidor
        
        let allSuccess = true;  // Variable para verificar si todas las pruebas son exitosas

        // Mostrar los resultados en el contenedor de logs
        data.results.forEach(result => {
            const logEntry = document.createElement('p');
            logEntry.innerHTML = `Acción: ${result.action}, Elemento: ${result.element}, Estado: ${result.status}`;
            logContainer.appendChild(logEntry);

            // Si alguna prueba falló, cambiar el estado de allSuccess
            if (result.status !== 'success') {
                allSuccess = false;
            }
        });

        // Mostrar el resultado final (check si todo es exitoso, X si alguna falla)
        const finalLogEntry = document.createElement('p');
        if (allSuccess) {
            finalLogEntry.innerHTML = `<span style="color: green;">✔️ Todas las acciones fueron exitosas</span>`;
        } else {
            finalLogEntry.innerHTML = `<span style="color: red;">❌ Algunas acciones fallaron</span>`;
        }
        logContainer.appendChild(finalLogEntry);
    })
    .catch(error => {
        console.error("Error en el fetch:", error);  // Captura y muestra cualquier error en el fetch
    });
});

// Función para añadir una fila de acción
function addRow() {
    const container = document.getElementById('actionContainer');
    const newRow = document.createElement('div');
    newRow.classList.add('action-row');
    newRow.innerHTML = `
        <div class="input-group">
            <select name="category[]" onchange="populateActions(this)">
                <option value="">Seleccione una categoría</option>
                <option value="navigation">Navigation</option>
                <option value="forms">Forms</option>
                <option value="alerts">Alerts</option>
                <option value="keyboard_mouse">Keyboard/Mouse</option>
                <option value="javascript">Javascript</option>
                <option value="data_extraction">Data Extraction</option>
                <option value="verifications">Verifications</option>
            </select>

            <select name="action[]" onchange="toggleInputField(this)">
                <option value="">Seleccione una acción</option>
            </select>
            
            <input type="text" name="element_type[]" placeholder="Tipo de elemento (e.g., name)">
            <input type="text" name="value[]" placeholder="Valor del selector (e.g., q)">
            <input type="text" name="input_value[]" placeholder="Texto a ingresar" style="display:none;">
        </div>
        <button type="button" class="delete-btn" onclick="removeRow(this)">✖</button>
    `;
    container.appendChild(newRow);
}

// Función para poblar las acciones según la categoría seleccionada
function populateActions(selectElement) {
    const category = selectElement.value;
    const actionSelect = selectElement.closest('.input-group').querySelector('select[name="action[]"]');
    actionSelect.innerHTML = '<option value="">Seleccione una acción</option>';

    if (actionCategories[category]) {
        actionCategories[category].forEach(action => {
            const option = document.createElement('option');
            option.value = action;
            option.textContent = action;
            actionSelect.appendChild(option);
        });
    }
}

// Función para eliminar una fila
function removeRow(button) {
    button.closest('.action-row').remove();
}

// Función para mostrar/ocultar input según la acción seleccionada
function toggleInputField(selectElement) {
    const inputGroup = selectElement.closest('.input-group');
    const elementTypeField = inputGroup.querySelector('input[name="element_type[]"]');
    const valueField = inputGroup.querySelector('input[name="value[]"]');
    const inputValueField = inputGroup.querySelector('input[name="input_value[]"]');
    const action = selectElement.value;

    const actionsWithoutElementTypeValue = ['accept_alert', 'confirm_alert', 'prompt_alert'];

    if (actionsWithoutElementTypeValue.includes(action)) {
        elementTypeField.style.display = "none";
        elementTypeField.required = false;
        valueField.style.display = "none";
        valueField.required = false;
        inputValueField.style.display = "none";
        inputValueField.required = false;
    } 
    else if (action === "enter_data" || action === "select") {
        elementTypeField.style.display = "block";
        elementTypeField.required = true;
        valueField.style.display = "block";
        valueField.required = true;
        inputValueField.style.display = "block";
        inputValueField.required = true;
        inputValueField.placeholder = action === "select" ? "Ingrese valor del select" : "Texto a ingresar";
    } 
    else if (action.startsWith("verify_")) {
        elementTypeField.style.display = "block";
        elementTypeField.required = true;
        valueField.style.display = "block";
        valueField.required = true;
        inputValueField.style.display = "block";
        inputValueField.required = true;
        inputValueField.placeholder = "Valor esperado";
    } 
    else {
        elementTypeField.style.display = "block";
        elementTypeField.required = true;
        valueField.style.display = "block";
        valueField.required = true;
        inputValueField.style.display = "none";
        inputValueField.required = false;
    }
}

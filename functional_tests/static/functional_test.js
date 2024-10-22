let executionCount = 0;  // Contador de ejecuciones
let currentTest = 1;  // Controla la prueba que está activa
let testCounter = 3;  // Controla el número total de pruebas creadas (3 por defecto)
const testsData = {};  // Almacena las acciones de cada prueba

// Inicializa con tres pruebas por defecto
testsData[1] = [];
testsData[2] = [];
testsData[3] = [];

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

        if (action === 'enter_data' || action === 'select') {
            const input_value = row.querySelector('input[name="input_value[]"]').value || null;
            actionData.input_value = input_value;
        }

        if (action.startsWith('verify_')) {
            const expected_value = row.querySelector('input[name="input_value[]"]').value || null;
            actionData.expected_value = expected_value;
        }

        actions.push(actionData);
    });

    if (!formIsValid) return;

    // Almacena las acciones para la prueba actual
    testsData[currentTest] = actions;

    // Crear los datos que vamos a enviar
    const data = {
        url: url,
        tests: testsData
    };

    console.log("Datos enviados al servidor:", data);  // Verifica que los datos se están preparando correctamente

    // Enviar los datos al servidor con fetch
    fetch('/tests/run/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos procesados:", data);

        let allSuccess = true;

        // Mostrar los resultados en el contenedor de logs
        data.results.forEach(result => {
            const logEntry = document.createElement('p');
            logEntry.innerHTML = `Acción: ${result.action}, Elemento: ${result.element}, Estado: ${result.status}`;
            logContainer.appendChild(logEntry);

            if (result.status !== 'success') {
                allSuccess = false;
            }
        });

        const finalLogEntry = document.createElement('p');
        if (allSuccess) {
            finalLogEntry.innerHTML = `<span style="color: green;">✔️ Todas las acciones fueron exitosas</span>`;
        } else {
            finalLogEntry.innerHTML = `<span style="color: red;">❌ Algunas acciones fallaron</span>`;
        }
        logContainer.appendChild(finalLogEntry);
    })
    .catch(error => {
        console.error("Error en el fetch:", error);
    });
});

function addTest() {
    // Encuentra el número más bajo disponible para una nueva prueba
    let newTestNumber = 1;
    while (testsData[newTestNumber]) {
        newTestNumber++; // Aumentar hasta encontrar un número que no esté en uso
    }

    const testList = document.getElementById('testList');
    const newTestDiv = document.createElement('div');
    
    newTestDiv.classList.add('test-item');
    newTestDiv.id = `test-${newTestNumber}`;
    newTestDiv.innerHTML = `<span>Prueba ${newTestNumber}</span> <button class="delete-btn" onclick="removeTest(${newTestNumber})">✖</button>`;
    newTestDiv.onclick = function () { showTest(newTestNumber); };

    testList.insertBefore(newTestDiv, document.getElementById('addTestBtn'));  // Añadir la prueba antes del botón de añadir prueba
    testsData[newTestNumber] = [];  // Inicializar las acciones de la nueva prueba
}


// Función para mostrar una prueba seleccionada y sus acciones
function showTest(testId) {
    currentTest = testId;

    // Cambiar el estado activo en la lista de pruebas
    document.querySelectorAll('.test-item').forEach(item => item.classList.remove('active'));
    document.getElementById(`test-${testId}`).classList.add('active');

    // Cargar las acciones de la prueba seleccionada
    const actionContainer = document.getElementById('actionContainer');
    actionContainer.innerHTML = '';  // Limpiar el contenedor de acciones

    if (testsData[testId].length > 0) {
        testsData[testId].forEach(actionData => {
            const newRow = createActionRow(actionData);
            actionContainer.appendChild(newRow);
        });
    } else {
        // Si no hay acciones, agregar una fila vacía
        addRow();
    }

    // Actualizar el título de la prueba
    document.getElementById('testTitle').innerText = `Prueba ${testId}`;
}


// Función para crear una fila de acción a partir de los datos
function createActionRow(actionData) {
    const newRow = document.createElement('div');
    newRow.classList.add('action-row');

    const actionSelectHTML = Object.entries(actionCategories).map(([category, actions]) => {
        return actions.map(action => `<option value="${action}" ${actionData.action === action ? 'selected' : ''}>${action}</option>`).join('');
    }).join('');

    newRow.innerHTML = `
        <div class="input-group">
            <select name="action[]">
                ${actionSelectHTML}
            </select>
            <input type="text" name="element_type[]" value="${actionData.element_type || ''}" placeholder="Tipo de elemento">
            <input type="text" name="value[]" value="${actionData.value || ''}" placeholder="Valor del selector">
            <input type="text" name="input_value[]" value="${actionData.input_value || ''}" placeholder="Texto a ingresar" style="${actionData.input_value ? 'block' : 'none'};">
        </div>
        <button type="button" class="delete-btn" onclick="removeRow(this)">✖</button>
    `;

    return newRow;
}

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
            
            <input type="text" name="element_type[]" placeholder="">
            <input type="text" name="value[]" placeholder="">
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

// Función para eliminar una prueba
function removeTest(testId) {
    delete testsData[testId];  // Eliminar la prueba de los datos

    const testElement = document.getElementById(`test-${testId}`);
    if (testElement) {
        testElement.remove();  // Eliminar visualmente el div de la prueba
    }

    // Si se eliminan todas las pruebas, añadir una nueva
    if (Object.keys(testsData).length === 0) {
        testCounter = 0;  // Reiniciar el contador si todas las pruebas fueron eliminadas
        addTest();  // Añadir una nueva prueba por defecto
    }
}

// Aseguramos que las pruebas 1, 2 y 3 también se puedan eliminar correctamente
function initializeDefaultTests() {
    for (let i = 1; i <= 3; i++) {
        document.getElementById(`test-${i}`).innerHTML = `<span>Prueba ${i}</span> <button class="delete-btn" onclick="removeTest(${i})">✖</button>`;
    }
}
// Llamamos a esta función para inicializar las pruebas por defecto al cargar la página
initializeDefaultTests();

// Función para actualizar el nombre de la prueba
function updateTestName(testId, newName) {
    document.querySelector(`#test-${testId} .test-name`).value = newName;
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

let executionCount = 0;  // Contador de ejecuciones
let currentTest = 1;  // Controla la prueba que está activa
let testCounter = 3;  // Controla el número total de pruebas creadas (3 por defecto)
const testsData = {};  // Almacena las acciones de cada prueba

// Inicializa con tres pruebas por defecto
testsData[1] = { actions: [] };  // Usamos un objeto con una propiedad 'actions'
testsData[2] = { actions: [] };
testsData[3] = { actions: [] };

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
// Función para validar si la URL es válida
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;  
    }
}
// Inicializa las pruebas por defecto y asigna eventos para poder eliminarlas
function initializeDefaultTests() {
    for (let i = 1; i <= 3; i++) {
        document.getElementById(`test-${i}`).innerHTML = `<span>Prueba ${i}</span> <button class="delete-btn" onclick="removeTest(${i})">✖</button>`;
        // Inicializamos los datos para cada prueba (vacío por defecto)
        testsData[i] = { url: '', actions: [] };
    }
}

// Llamamos a esta función para inicializar las pruebas por defecto al cargar la página
initializeDefaultTests();

// Función para guardar la URL y acciones de la prueba actual
function saveCurrentTest() {
    const url = document.getElementById('url').value;  // Capturar la URL actual
    const actions = [];  // Aquí guardaremos las acciones
}

// Manejador de evento para enviar el formulario
document.getElementById('testForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar el envío predeterminado del formulario

    executionCount += 1;  // Aumentar el contador global

    const url = document.getElementById('url').value;
    const logContainer = document.getElementById('log-output');
    logContainer.innerHTML = '';  // Limpiar logs anteriores

    const actions = [];
    let formIsValid = true;

    // Validar que la URL esté presente y sea válida
    if (!url || !isValidUrl(url)) {
        alert("Por favor, ingresa una URL válida.");
        return;
    }

    // Recorre todas las filas de acción y agrega las acciones al array 'actions'
    document.querySelectorAll('#actionContainer .action-row').forEach((row) => {
        const action = row.querySelector('select[name="action[]"]').value;
        const element_type = row.querySelector('input[name="element_type[]"]').value;
        const value = row.querySelector('input[name="value[]"]').value;

        const actionsWithoutElementTypeValue = ['accept_alert', 'confirm_alert', 'prompt_alert'];
        if (!actionsWithoutElementTypeValue.includes(action) && (!element_type || !value)) {
            alert("Por favor, asegúrate de que todos los campos estén llenos.");
            formIsValid = false;
            return;
        }

        let actionData = { action };

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

     // Almacenar la URL y las acciones para la prueba actual
    testsData[currentTest] = { url: url, actions: actions };  // URL específica para cada prueba
    // Filtrar y enviar solo las pruebas que tengan acciones y URL válidas
    const data = Object.keys(testsData)
        .filter(testId => testsData[testId].actions.length > 0 && isValidUrl(testsData[testId].url))
        .map(testId => ({
            url: testsData[testId].url,
            actions: testsData[testId].actions
        }));

    console.log("Datos que se enviarán:", JSON.stringify(data));

    // Enviar los datos con fetch
    fetch('/tests/run/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value  // Incluye el token CSRF
        },
        body: JSON.stringify(data)  // Enviar el JSON con los datos de la prueba
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                logContainer.innerHTML = `<span style="color: red;">Error en el servidor: ${errorData.error || 'Error desconocido'}</span>`;
                console.error("Error en la respuesta del servidor:", errorData);
                throw new Error('Error en el servidor');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Datos procesados:", data);

        logContainer.innerHTML = '';  // Limpiar logs anteriores

        if (data.individual_results && Array.isArray(data.individual_results)) {
            let allSuccess = true;
            const totalResults = data.individual_results.length;
            const successfulResults = data.individual_results.filter(result => result.result === 'success').length;

            data.individual_results.forEach(result => {
                const logEntry = document.createElement('p');
                logEntry.innerHTML = `Acción: ${result.actions.map(a => a.action)}, Estado: ${result.result}`;
                logContainer.appendChild(logEntry);

                if (result.result !== 'success') {
                    allSuccess = false;
                }
            });

            const finalLogEntry = document.createElement('p');
            finalLogEntry.innerHTML = successfulResults === totalResults
                ? `<span style="color: green;">✔️ Todas las acciones (${successfulResults}/${totalResults}) fueron exitosas</span>`
                : `<span style="color: red;">❌ ${totalResults - successfulResults} de ${totalResults} acciones fallaron</span>`;
            logContainer.appendChild(finalLogEntry);
        } else {
            console.error("El objeto 'individual_results' no existe o no es un array:", data);
            const errorEntry = document.createElement('p');
            errorEntry.innerHTML = `<span style="color: red;">Error: No se recibieron resultados válidos</span>`;
            logContainer.appendChild(errorEntry);
        }
    })
    .catch(error => {
        console.error("Error en el fetch:", error);
        const errorEntry = document.createElement('p');
        errorEntry.innerHTML = `<span style="color: red;">Error al procesar las pruebas: ${error.message}</span>`;
        logContainer.appendChild(errorEntry);
    });
});

// Función para agregar una nueva prueba
function addTest() {
    let newTestNumber = 1;
    while (testsData[newTestNumber]) {
        newTestNumber++;  // Encuentra el número de prueba más bajo disponible
    }

    const testList = document.getElementById('testList');
    const newTestDiv = document.createElement('div');
    
    newTestDiv.classList.add('test-item');
    newTestDiv.id = `test-${newTestNumber}`;
    newTestDiv.innerHTML = `<span>Prueba ${newTestNumber}</span> <button class="delete-btn" onclick="removeTest(${newTestNumber})">✖</button>`;
    newTestDiv.onclick = function () { showTest(newTestNumber); };

    testList.insertBefore(newTestDiv, document.getElementById('addTestBtn'));
    testsData[newTestNumber] = { url: '', actions: [] };  // Inicializar la nueva prueba
}

// Función para mostrar la prueba seleccionada
function showTest(testId) {
    // Guardar la prueba actual antes de cambiar a una nueva prueba
    saveCurrentTest();

    // Actualizar el ID de la prueba actual
    currentTest = testId;

    // Cargar los datos de la nueva prueba desde testsData
    const testData = testsData[testId];

    // Cargar la URL en el campo correspondiente
    document.getElementById('url').value = testData.url || '';  // Si no tiene URL, dejar vacío

    // Limpiar el contenedor de acciones
    const actionContainer = document.getElementById('actionContainer');
    actionContainer.innerHTML = '';

    // Cargar cada acción guardada de la prueba en la interfaz
    if (testData.actions.length > 0) {
        testData.actions.forEach((actionData) => {
            const newRow = createActionRow(actionData);  // Crear una fila con los datos de la acción
            actionContainer.appendChild(newRow);  // Añadir la fila de acción
        });
    } else {
        addRow();  // Si no hay acciones, agregar una fila vacía
    }
}
// Función para crear una fila de acción
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

// Función para eliminar una prueba

function removeRow(button) {
    button.closest('.action-row').remove();
}

// Función para eliminar una prueba
function removeTest(testId) {
    const testElement = document.getElementById(`test-${testId}`);
    if (testElement) {
        testElement.remove();  // Eliminar el elemento del DOM
    }
    delete testsData[testId];  // Eliminar la prueba de los datos
}


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
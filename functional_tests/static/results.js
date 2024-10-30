// Objeto para almacenar los datos de cada prueba
const testsData = {};
let currentTest = null;

// Función para agregar una nueva prueba
function addTest() {
  let newTestNumber = 1;
  while (testsData[newTestNumber]) {
    newTestNumber++; // Encuentra el número de prueba más bajo disponible
  }

  const testList = document.getElementById("testList");
  const newTestDiv = document.createElement("div");

  newTestDiv.classList.add("test-item");
  newTestDiv.id = `test-${newTestNumber}`;
  newTestDiv.innerHTML = `
        <input type="text" value="Prueba ${newTestNumber}" class="test-name" oninput="updateTestName(${newTestNumber}, this.value)">
        <button type="button" class="delete-btn" onclick="removeTest(${newTestNumber})">✖</button>
    `;
  newTestDiv.onclick = function () {
    showTest(newTestNumber);
  };

  testList.insertBefore(newTestDiv, document.getElementById("addTestBtn"));
  testsData[newTestNumber] = { url: "", actions: [] }; // Inicializar la nueva prueba
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
  document.getElementById("url").value = testData.url || ""; // Si no tiene URL, dejar vacío

  // Limpiar el contenedor de acciones
  const actionContainer = document.getElementById("actionContainer");
  actionContainer.innerHTML = "";

  // Cargar cada acción guardada de la prueba en la interfaz
  if (testData.actions.length > 0) {
    testData.actions.forEach((actionData) => {
      const newRow = createActionRow(actionData); // Crear una fila con los datos de la acción
      actionContainer.appendChild(newRow); // Añadir la fila de acción
    });
  } else {
    addRow(); // Si no hay acciones, agregar una fila vacía
  }
}

// Función para actualizar el nombre de la prueba
function updateTestName(testId, newName) {
  document.querySelector(`#test-${testId} .test-name`).value = newName;
}

// Función para guardar la prueba actual en testsData
function saveCurrentTest() {
  if (currentTest !== null) {
    const url = document.getElementById("url").value;
    const actions = [];

    // Obtener todas las filas de acción y guardar los datos
    document.querySelectorAll("#actionContainer .action-row").forEach((row) => {
      const action = {
        category: row.querySelector('[name="category[]"]').value,
        action: row.querySelector('[name="action[]"]').value,
        element_type: row.querySelector('[name="element_type[]"]').value,
        value: row.querySelector('[name="value[]"]').value,
        input_value: row.querySelector('[name="input_value[]"]').value || null,
      };
      actions.push(action);
    });

    // Actualizar datos de la prueba actual en testsData
    testsData[currentTest] = { url, actions };
  }
}


// Función para eliminar una prueba
function removeTest(testId) {
  document.getElementById(`test-${testId}`).remove();
  delete testsData[testId];
  if (currentTest === testId) {
    currentTest = null;
    document.getElementById("url").value = "";
    document.getElementById("actionContainer").innerHTML = "";
  }
}





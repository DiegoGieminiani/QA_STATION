// Función para inicializar los gráficos en results.html
function initializeCharts(results) {
    const successCount = results.filter(result => result.status === "success").length;
    const failCount = results.filter(result => result.status === "fail").length;

    const total = successCount + failCount;

    // Gráfico de Pastel (Pie Chart) con porcentajes
    const ctxPie = document.getElementById('statusPieChart').getContext('2d');
    new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: ['Éxitos', 'Fallos'],
            datasets: [{
                data: [successCount, failCount],
                backgroundColor: ['#4CAF50', '#FF6347']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let value = tooltipItem.raw;
                            let percentage = ((value / total) * 100).toFixed(2);
                            return `${tooltipItem.label}: ${percentage}% (${value})`;
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Barras (Bar Chart) para mostrar el conteo de cada tipo de Acción
    const actionCounts = {};
    results.forEach(result => {
        const action = result.action;
        actionCounts[action] = (actionCounts[action] || 0) + 1;
    });

    const ctxBar = document.getElementById('actionBarChart').getContext('2d');
    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: Object.keys(actionCounts),
            datasets: [{
                label: 'Cantidad de Acciones',
                data: Object.values(actionCounts),
                backgroundColor: '#4CAF50'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

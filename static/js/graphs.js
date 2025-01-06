document.addEventListener('DOMContentLoaded', () => {
    const variables = [
        { name: 'Temperature Front (°C)', key: 'temperature_front' },
        { name: 'Temperature Back (°C)', key: 'temperature_back' },
        { name: 'Current TEG (A)', key: 'current_teg' },
        { name: 'Current Solar (A)', key: 'current_solar' },
        { name: 'Voltage Solar (V)', key: 'voltage_solar' },
        { name: 'Voltage TEG (V)', key: 'voltage_teg' },
        { name: 'Power Solar (W)', key: 'power_solar' },
        { name: 'Power TEG (W)', key: 'power_teg' }
    ];

    // Populate select elements
    const xAxisSelect = document.getElementById('x-axis');
    const yAxisSelect = document.getElementById('y-axis');
    variables.forEach(variant => {
        const xOption = document.createElement('option');
        xOption.value = variant.key;
        xOption.textContent = variant.name;
        xAxisSelect.appendChild(xOption);

        const yOption = document.createElement('option');
        yOption.value = variant.key;
        yOption.textContent = variant.name;
        yAxisSelect.appendChild(yOption);
    });

    // Declare scatterChart variable
    let scatterChart;

    // Function to fetch data
    function fetchData(xVar, yVar) {
        fetch('/graph_data')
            .then(response => response.json())
            .then(data => {
                // Filter data points with null values for selected variables
                const filteredData = data.filter(entry =>
                    entry[xVar] !== null && entry[yVar] !== null
                );
                // Extract x and y data
                const xData = filteredData.map(entry => entry[xVar]);
                const yData = filteredData.map(entry => entry[yVar]);
                // Update the chart
                updateChart(xData, yData, xVar, yVar);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to update the chart
    function updateChart(xData, yData, xVar, yVar) {
        const ctx = document.getElementById('scatterChart').getContext('2d');
        if (scatterChart) {
            scatterChart.destroy();
        }
        scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: `${yVar} vs ${xVar}`,
                    data: xData.map((x, index) => ({ x: x, y: yData[index] })),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)'
                }]
            },
            options: {
                scales: {
                    x: {
                        title: { display: true, text: xVar },
                        type: 'linear'
                    },
                    y: {
                        title: { display: true, text: yVar },
                        type: 'linear'
                    }
                }
            }
        });
    }

    // Event listener for select changes
    xAxisSelect.addEventListener('change', () => {
        const xVar = xAxisSelect.value;
        const yVar = yAxisSelect.value;
        if (xVar && yVar) {
            fetchData(xVar, yVar);
        }
    });

    yAxisSelect.addEventListener('change', () => {
        const xVar = xAxisSelect.value;
        const yVar = yAxisSelect.value;
        if (xVar && yVar) {
            fetchData(xVar, yVar);
        }
    });

    // Initial chart load
    const defaultXVar = variables[0].key;
    const defaultYVar = variables[1].key;
    fetchData(defaultXVar, defaultYVar);
});
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
    let currentData = []; // Store the current data for analysis

    // Function to fetch data
    function fetchData(xVar, yVar) {
        fetch('/graph_data')
            .then(response => response.json())
            .then(data => {
                const filteredData = data.filter(entry =>
                    entry[xVar] !== null && entry[yVar] !== null
                );
                const xData = filteredData.map(entry => entry[xVar]);
                const yData = filteredData.map(entry => entry[yVar]);
                currentData = filteredData.slice(-20); // Store the last 20 data points
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

    // Gemini AI Analysis
    const analyzeButton = document.getElementById('analyzeButton');
    const geminiResponse = document.getElementById('geminiResponse');

    analyzeButton.addEventListener('click', async () => {
        const xVar = xAxisSelect.value;
        const yVar = yAxisSelect.value;

        if (!currentData.length) {
            geminiResponse.textContent = "No data available for analysis.";
            return;
        }

        // Prepare the data for Gemini
        const dataForAnalysis = currentData.map(entry => ({
            [xVar]: entry[xVar],
            [yVar]: entry[yVar]
        }));

        // Prepare the prompt for Gemini
        const prompt = `
        Analyze the following data and provide insights:
        - X-axis: ${xVar}
        - Y-axis: ${yVar}
        - Data: ${JSON.stringify(dataForAnalysis, null, 2)}

        Examples of good analysis:
        1. "The data shows a strong positive correlation between X and Y, indicating that as X increases, Y also increases."
        2. "There is no clear relationship between X and Y, suggesting that other factors may be influencing the results."
        3. "The data exhibits a cyclical pattern, which could indicate periodic behavior in the system."

        Based on the data, provide a detailed analysis.
        `;

        // Send the prompt to Gemini
        try {
            const response = await fetch('/analyze_with_gemini', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const result = await response.json();
            geminiResponse.textContent = result.response;
        } catch (error) {
            console.error('Error analyzing data with Gemini:', error);
            geminiResponse.textContent = "Failed to analyze data. Please try again.";
        }
    });
});
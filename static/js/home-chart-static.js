document.addEventListener('DOMContentLoaded', () => {
    console.log('Chart logic loaded'); // Debugging

    // Initialize the line chart
    const ctx = document.getElementById('lineChart').getContext('2d');
    const lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Time labels
            datasets: [
                { label: 'Temperature Front (°C)', data: [], borderColor: 'red', fill: false },
                { label: 'Temperature Back (°C)', data: [], borderColor: 'orange', fill: false },
                { label: 'Current TEG (A)', data: [], borderColor: 'blue', fill: false },
                { label: 'Current Solar (A)', data: [], borderColor: 'green', fill: false },
                { label: 'Voltage Solar (V)', data: [], borderColor: 'purple', fill: false },
                { label: 'Voltage TEG (V)', data: [], borderColor: 'pink', fill: false },
                { label: 'Power Solar (W)', data: [], borderColor: 'yellow', fill: false },
                { label: 'Power TEG (W)', data: [], borderColor: 'brown', fill: false }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: { unit: 'second' },
                    title: { display: true, text: 'Time' }
                },
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Values' }
                }
            },
            animation: {
                duration: 0 // Disable animation for smoother updates
            }
        }
    });

    // Function to update the chart with new data
    function updateChart(data) {
        const currentTime = new Date(); // Use Date object for time-based charts

        // Append new data points to the chart
        lineChart.data.labels.push(currentTime);
        lineChart.data.datasets[0].data.push(data.temperature_front);
        lineChart.data.datasets[1].data.push(data.temperature_back);
        lineChart.data.datasets[2].data.push(data.current_teg);
        lineChart.data.datasets[3].data.push(data.current_solar);
        lineChart.data.datasets[4].data.push(data.voltage_solar);
        lineChart.data.datasets[5].data.push(data.voltage_teg);
        lineChart.data.datasets[6].data.push(data.power_solar);
        lineChart.data.datasets[7].data.push(data.power_teg);

        // Optional: Limit the number of data points to avoid performance issues
        if (lineChart.data.labels.length > 100) { // Change 100 to any number you prefer
            lineChart.data.labels.shift(); // Remove the oldest label
            lineChart.data.datasets.forEach(dataset => dataset.data.shift()); // Remove the oldest data point
        }

        // Update the chart
        lineChart.update();
    }

    // Function to fetch data and update the chart
    function fetchChartData() {
        console.log('Fetching chart data...'); // Debugging
        fetch('/data') // Ensure this endpoint returns the expected JSON
            .then(response => response.json())
            .then(data => {
                console.log('Chart data received:', data); // Debugging
                updateChart(data);
            })
            .catch(error => console.error('Error fetching chart data:', error));
    }

    // Fetch data immediately after page loads
    fetchChartData();

    // Continue to fetch data every second
    setInterval(fetchChartData, 1000);
});
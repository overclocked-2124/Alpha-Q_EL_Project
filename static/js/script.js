// Initialize arrays to store sensor data for graphing
let voltageData = [];
let currentData = [];
let temperatureData = [];

// Get references to the HTML elements
const voltageElement = document.getElementById('voltage');
const currentElement = document.getElementById('current');
const temperatureElement = document.getElementById('temperature');

// Set up the Chart.js line chart
const ctx = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Time labels will be added dynamically
        datasets: [
            {
                label: 'Voltage (V)',
                data: voltageData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            },
            {
                label: 'Current (A)',
                data: currentData,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
            },
            {
                label: 'Temperature (°C)',
                data: temperatureData,
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom'
            }
        }
    }
});

// Function to fetch data from the Flask backend
function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Update the HTML elements with the latest data
            voltageElement.textContent = data.voltage.toFixed(2) + ' V';
            currentElement.textContent = data.current.toFixed(2) + ' A';
            temperatureElement.textContent = data.temperature.toFixed(2) + ' °C';

            // Update the chart data
            const currentTime = new Date().toLocaleTimeString();
            lineChart.data.labels.push(currentTime);
            voltageData.push(data.voltage);
            currentData.push(data.current);
            temperatureData.push(data.temperature);

            // Limit the number of data points displayed
            if (voltageData.length > 20) {
                voltageData.shift();
                currentData.shift();
                temperatureData.shift();
                lineChart.data.labels.shift();
            }

            // Update the chart
            lineChart.update();
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Fetch data every second
setInterval(fetchData, 1000);
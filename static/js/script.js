document.addEventListener('DOMContentLoaded', () => {
    // Select the canvas element
    const ctx = document.getElementById('lineChart').getContext('2d');

    // Create the line chart
    const lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Time labels
            datasets: [
                {
                    label: 'Temperature Front (°C)',
                    data: [],
                    borderColor: 'red',
                    fill: false,
                },
                {
                    label: 'Temperature Back (°C)',
                    data: [],
                    borderColor: 'orange',
                    fill: false,
                },
                {
                    label: 'Current TEG (A)',
                    data: [],
                    borderColor: 'blue',
                    fill: false,
                },
                {
                    label: 'Current Solar (A)',
                    data: [],
                    borderColor: 'green',
                    fill: false,
                },
                {
                    label: 'Voltage Solar (V)',
                    data: [],
                    borderColor: 'purple',
                    fill: false,
                },
                {
                    label: 'Voltage TEG (V)',
                    data: [],
                    borderColor: 'pink',
                    fill: false,
                },
                {
                    label: 'Power Solar (W)',
                    data: [],
                    borderColor: 'yellow',
                    fill: false,
                },
                {
                    label: 'Power TEG (W)',
                    data: [],
                    borderColor: 'brown',
                    fill: false,
                },
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Values'
                    }
                }
            }
        }
    });

    // Fetch data and update chart
    function fetchData() {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                const currentTime = new Date().toLocaleTimeString();

                // Update labels and datasets
                lineChart.data.labels.push(currentTime);
                lineChart.data.datasets[0].data.push(data.temperature_front);
                lineChart.data.datasets[1].data.push(data.temperature_back);
                lineChart.data.datasets[2].data.push(data.current_teg);
                lineChart.data.datasets[3].data.push(data.current_solar);
                lineChart.data.datasets[4].data.push(data.voltage_solar);
                lineChart.data.datasets[5].data.push(data.voltage_teg);
                lineChart.data.datasets[6].data.push(data.power_solar);
                lineChart.data.datasets[7].data.push(data.power_teg);

                // Limit data points to 50
                if (lineChart.data.labels.length > 50) {
                    lineChart.data.labels.shift();
                    lineChart.data.datasets.forEach(dataset => dataset.data.shift());
                }

                lineChart.update();
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Fetch data every second
    setInterval(fetchData, 1000);
});

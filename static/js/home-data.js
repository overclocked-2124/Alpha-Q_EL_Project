document.addEventListener('DOMContentLoaded', () => {
    console.log('Data logic loaded'); // Debugging

    // Function to update the card values
    function updateCardValues(data) {
        console.log('Updating card values with:', data); // Debugging
        document.getElementById('temperature-front').textContent = data.temperature_front.toFixed(2);
        document.getElementById('temperature-back').textContent = data.temperature_back.toFixed(2);
        document.getElementById('current-teg').textContent = data.current_teg.toFixed(2);
        document.getElementById('current-solar').textContent = data.current_solar.toFixed(2);
        document.getElementById('voltage-solar').textContent = data.voltage_solar.toFixed(2);
        document.getElementById('voltage-teg').textContent = data.voltage_teg.toFixed(2);
        document.getElementById('power-solar').textContent = data.power_solar.toFixed(2);
        document.getElementById('power-teg').textContent = data.power_teg.toFixed(2);
        document.getElementById('irradience-front').textContent = data.irradience_front.toFixed(2);
        document.getElementById('irradience-back').textContent = data.irradience_back.toFixed(2);
        document.getElementById('irradience-onsolar').textContent = data.irradience_onsolar.toFixed(2);
    }

    // Function to fetch data and update the card values
    function fetchData() {
        console.log('Fetching data...'); // Debugging
        fetch('/data') // Ensure this endpoint returns the expected JSON
            .then(response => response.json())
            .then(data => {
                console.log('Data received:', data); // Debugging
                updateCardValues(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Fetch data immediately after page loads
    fetchData();

    // Continue to fetch data every second
    setInterval(fetchData, 1000);
});
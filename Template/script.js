// Doughnut Chart for Efficiency Card
const efficiencyCtx = document.getElementById('efficiencyChart').getContext('2d');
new Chart(efficiencyCtx, {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [58, 42],
            backgroundColor: ['#7a5cff', '#e0e0e0'],
            borderWidth: 2,
        }]
    },
    options: {
        cutout: '80%',
        responsive: false,
        plugins: {
            legend: { display: false }
        }
    }
});

// Area Chart for "IN SPACE"
const spaceCtx = document.getElementById('spaceChart').getContext('2d');
new Chart(spaceCtx, {
    type: 'line',
    data: {
        labels: Array.from({ length: 10 }, (_, i) => i),
        datasets: [{
            label: 'Dataset 1',
            data: [10, 8, 6, 7, 5, 3, 4, 6, 7, 8],
            borderColor: '#7a5cff',
            backgroundColor: 'rgba(122, 92, 255, 0.3)',
            fill: true
        }, {
            label: 'Dataset 2',
            data: [5, 3, 4, 6, 2, 8, 6, 5, 4, 7],
            borderColor: 'rgba(250, 100, 100, 0.5)',
            backgroundColor: 'rgba(250, 100, 100, 0.3)',
            fill: true
        }]
    },
    options: {
        responsive: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Line Chart
const lineCtx = document.getElementById('lineChart').getContext('2d');
new Chart(lineCtx, {
    type: 'line',
    data: {
        labels: Array.from({ length: 30 }, (_, i) => i + 1),
        datasets: [{
            label: 'Data',
            data: [500, 800, 200, 600, 300, 400, 700, 300, 650, 500, 900, 750, 300, 600, 800, 1000, 400, 600, 800, 500, 700, 650, 850, 900, 400, 600, 700, 500, 800, 200],
            borderColor: '#7a5cff',
            backgroundColor: 'rgba(122, 92, 255, 0.2)',
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: '#7a5cff',
            pointBorderColor: '#ffffff',
            tension: 0.2,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});


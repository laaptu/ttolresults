// chartWrapper.js

class ChartWrapper {
    constructor(label) {
        this.label = label;
        this.chartInstance = null;
    }

    refresh(data) {
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }

        this.chartInstance = new Chart(document.getElementById(this.label), {
            type: 'bar',
            data: {
                labels: data.numbers,
                datasets: [{
                    label: this.label,
                    data: data.occurrences,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    datalabels: {
                        align: 'end',
                        anchor: 'end',
                        color: '#555',
                        formatter: (value, context) => value
                    }
                }
            }
        });
    }
}

const categoriesLastMonthChart = document.getElementById('categories-last-month-graph');
const expenseSumPerMonthChart = document.getElementById('expense-sum-per-month-graph');
const budgetsRealizationChart = document.getElementById('budgets-realization-graph');

const categoriesSpentLastMonthData = getData(_categories_spent)
const expenseSumPerMonthData= getData(_expense_sum_per_month)
const budgetRealizationData= getData(_budgets_realization)

function getData(data) {
    return JSON.parse(data)
}

const autocolors = window['chartjs-plugin-autocolors'];
const lighten = (color, value) => Chart.helpers.color(color).lighten(value).rgbString();
Chart.register(autocolors);


new Chart(categoriesLastMonthChart,
    {
        type: 'doughnut',
        data: {
            labels: categoriesSpentLastMonthData.map(row => row.name),
            datasets: [{
                data: categoriesSpentLastMonthData.map(row => row.sum)
            }]
        },
        options: {
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                autocolors: {
                    mode: 'data',
                    offset: 2
                },
                legend: {
                    display: true,
                    labels: {
                        color: '#FFFFFF',
                    }
                }
            },
        }
    }
);

new Chart(budgetsRealizationChart,
    {
        type: 'polarArea',
        data: {
            labels: budgetRealizationData.map(row => row.name),
            datasets: [{
                data: budgetRealizationData.map(row => row.realization)
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                autocolors: {
                    mode: 'data',
                    offset: 4
                },
                legend: {
                    display: true,
                    labels: {
                        color: '#FFFFFF'
                    }
                }
            },
            scales: {
                r: {
                    grid: {
                        color: '#666'
                    },
                    ticks: {
                        color: '#888',
                        backdropColor: 'rgba(0, 0, 0, 0.0)',
                    }
                }
            },
            elements: {
                arc: {
                    borderColor: "#666"
                }
            }
        }
    }
);

new Chart(expenseSumPerMonthChart,
    {
        type: 'bar',
        data: {
            labels: expenseSumPerMonthData.map(row => row.month),
            datasets: [{
                data: expenseSumPerMonthData.map(row => row.spent)
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                autocolors: {
                    offset: 5
                },
                legend: {
                    display: false
                },
            },
            scales: {
                x: {
                    grid: {
                        color: '#666'
                    }
                },
                y: {
                    grid: {
                        color: '#666'
                    }
                }
            }
        }
    }
);

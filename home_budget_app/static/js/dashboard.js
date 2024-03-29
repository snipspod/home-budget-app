const categoriesLastMonthCanv = document.getElementById('categories-last-month-graph');
const expenseSumPerMonthCanv = document.getElementById('expense-sum-per-month-graph');
const budgetsRealizationCanv = document.getElementById('budgets-realization-graph');

const categoriesSpentLastMonthData = getData(_categories_spent)
const expenseSumPerMonthData= getData(_expense_sum_per_month)
const budgetRealizationData= getData(_budgets_realization)
const budgetRealizationMonthInput = document.querySelector('#budget-realization-month')

budgetRealizationMonthInput.value = getCurrentDate()

function getData(data) {
    return JSON.parse(data)
}

const autocolors = window['chartjs-plugin-autocolors'];
const lighten = (color, value) => Chart.helpers.color(color).lighten(value).rgbString();
Chart.register(autocolors);


const categoriesLastMonthChart =  new Chart(categoriesLastMonthCanv,
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

const budgetsRealizationChart = new Chart(budgetsRealizationCanv,
    {
        type: 'polarArea',
        data: {
            labels: budgetRealizationData.find(o => o.date == getCurrentDate()).budgets.map(row => row.name),
            datasets: [{
                data: budgetRealizationData.find(o => o.date == getCurrentDate()).budgets.map(row => row.realization)
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


const expenseSumPerMonthChart = new Chart(expenseSumPerMonthCanv,
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

budgetRealizationMonthInput.addEventListener('change', (event) => {
    date = event.currentTarget.value.toString()

    let obj = budgetRealizationData.find(o => o.date == date).budgets

    budgetsRealizationChart.config.data.labels = obj.map(row => row.name)
    budgetsRealizationChart.config.data.datasets = [{data: obj.map(row => row.realization)}]
    budgetsRealizationChart.update()

    
})

function getCurrentDate() {
    currentDate = new Date()

    year = currentDate.getFullYear().toString()
    month = currentDate.getMonth()+1

    if (month < 10) {
        month = `0${month.toString()}`
    } else {
        month = month.toString()
    }

    return `${year}-${month}`
}
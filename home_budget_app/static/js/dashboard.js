const ctx = document.getElementById('sampleChart');

const categoriesSpent = getData(_categories_spent)
console.log(categoriesSpent)

function getData(data) {
    return JSON.parse(data)
}

  new Chart(
    ctx,
    {
        type: 'doughnut',
        data: {
            labels: categoriesSpent.map(row => row.name),
            datasets: [
                {
                    data: categoriesSpent.map(row => row.sum)
                }
            ]
        },
        options: {
            animation: false,
            plugins:{
                legend: {
                    display: true,
                    labels: {
                        color: '#FFFFFF',
                        borderColor: "#000000"
                    }
                }
            }
        }
    }
  );

let tableRows = document.querySelectorAll('.expenseTableRow')
let amount = document.querySelector('#amount')
let category = document.querySelector('#category')
let date = document.querySelector('#date')
let account = document.querySelector('#account')
let description = document.querySelector('#description')
let expenseId = document.querySelectorAll('#expense_id')

let table = new DataTable('#expenses', {
    columnDefs: [
        { orderable: false, targets: 6 }
    ]
})

tableRows.forEach(row => {
    row.addEventListener('click', () => {
        amount.value = row.dataset.amount.replace('.', ',')
        date.value = row.dataset.date
        description.value = row.dataset.description
        expenseId.forEach(field => {
            field.value = row.dataset.expenseid
        })
    })
});
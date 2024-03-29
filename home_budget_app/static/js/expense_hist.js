let tableRows = document.querySelectorAll('.expenseTableRow')
let amount = document.querySelector('#amount')
let category = document.querySelector('#category')
let date = document.querySelector('#date')
let account = document.querySelector('#account')
let description = document.querySelector('#description')
let expenseId = document.querySelectorAll('#expense_id')

let table = new DataTable('#expenses', {
    responsive: true,
    columnDefs: [
        { responsivePriority: 1, orderable: false, targets: 6 },
        { targets: 2, render: DataTable.render.ellipsis( 15, true ) }
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
        category.value = row.dataset.categoryid
        account.value = row.dataset.accountid
    })
});
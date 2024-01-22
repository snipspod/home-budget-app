document.addEventListener('DOMContentLoaded', () => {
    let table = new DataTable('#expenses', {
        columnDefs: [
            { orderable: false, targets: 6 }
        ]
    })
} ,false)

let tableRows = document.getElementsByClassName('expenseTableRow')
let amount = document.querySelector('#amount')
let category = document.querySelector('#category')
let date = document.querySelector('#date')
let account = document.querySelector('#account')
let description = document.querySelector('#description')
let expenseId = document.querySelectorAll('#expense_id')
// let btnDeleteExpense = document.querySelector('#btnDeleteExpense')



Array.from(tableRows).forEach(row => {
    row.addEventListener('click', () => {
        amount.value = row.dataset.amount.replace('.', ',')
        category.value = row.dataset.category
        date.value = row.dataset.date
        account.value = row.dataset.account
        description.value = row.dataset.description
        Array.from(expenseId).forEach(field => {
            field.value = row.dataset.expenseid
        })
    })
});

// btnDeleteExpense.addEventListener('click', () => {
//     fetch('/expenses/delete', {
//         method: 'DELETE',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded'
//         },
//         'redirect': 'follow'
//     })
// })



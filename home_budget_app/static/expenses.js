document.addEventListener('DOMContentLoaded', () => {
    let table = new DataTable('#expenses');
} ,false)

let tableRows = document.getElementsByClassName('expenseTableRow')
let amount = document.querySelector('#amount')
let category = document.querySelector('#category')
let date = document.querySelector('#date')
let account = document.querySelector('#account')
let description = document.querySelector('#description')
let expenseId = document.querySelector('#expense_id')



Array.from(tableRows).forEach(row => {
    row.addEventListener('click', () => {
        amount.value = row.dataset.amount.replace('.', ',')
        category.value = row.dataset.category
        date.value = row.dataset.date
        account.value = row.dataset.account
        description.value = row.dataset.description
        expenseId.value = row.dataset.expenseid
    })
});

// console.log(data)

// let modal = document.getElementById('modalEdit')
// let amount
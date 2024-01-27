let tableRows = document.querySelectorAll('.expenseTableRow')
let amount = document.querySelector('#amount')
let category = document.querySelector('#category')
let date = document.querySelector('#date')
let account = document.querySelector('#account')
let description = document.querySelector('#description')
let expenseId = document.querySelectorAll('#expense_id')


let btnDelRow = document.querySelector("#btnDelRow")
let addRowBtns = document.querySelectorAll('.btnAddRow')



document.addEventListener('DOMContentLoaded', () => {
    let table = new DataTable('#expenses', {
        columnDefs: [
            { orderable: false, targets: 6 }
        ]
    })
} ,false)


tableRows.forEach(row => {
    row.addEventListener('click', () => {
        amount.value = row.dataset.amount.replace('.', ',')
        category.value = row.dataset.category
        date.value = row.dataset.date
        account.value = row.dataset.account
        description.value = row.dataset.description
        expenseId.forEach(field => {
            field.value = row.dataset.expenseid
        })
    })
});

btnDelRow.addEventListener('click', () => {
    alert('hej')
})

addRowBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        addTableRow()
    })
})

function addTableRow() {
    let addExpenseTable = document.querySelector("#addExpensesTable")
    let addExpenseTableBody = document.querySelector("#addExpensesTableBody")

    console.log(addExpenseTableBody.rows.item(addExpenseTableBody.rows.length - 1))
    console.log(parseInt(addExpenseTableBody.rows.item(addExpenseTableBody.rows.length - 1).firstElementChild.textContent) + 1)
    let newRow = addExpenseTable.insertRow(-1)
    let orderNumber = newRow.insertCell(0)

    orderNumber.innerText = `1`

    let cell2 = newRow.insertCell(1)
    cell2.innerHTML = `<input type="text" id="amount" name="amount" placeholder="0" 
    pattern="^(([1-9]\d{0,2}(\d{3})*)|\d+)?(,\d{1,2})?$"
    title="Podaj wartość całkowitą, lub po przecinku np. 0,25, 30, 21,3"
    class="form-control" required>`

    let cell3 = newRow.insertCell(2)
    cell3.innerHTML = `<input type="text" id="description" name="description" pattern="^(\S| ){1,100}$" title="Opis nie może być pusty i może zawierać maksymalnie 100 znaków" class="form-control">`

    let cell4 = newRow.insertCell(3)
    cell4.innerHTML = ``
    
    let cell5 = newRow.insertCell(4)
    let cell6 = newRow.insertCell(5)
    let cell7 = newRow.insertCell(6)

}

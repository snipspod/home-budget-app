let btnDelRows = document.querySelectorAll(".btnDelRow")
let addRowBtns = document.querySelectorAll('.btnAddRow')

const categories = getData(_categories)
const accounts = getData(_accounts)
const dateNow = getData(_date)

btnDelRows.forEach(btn => {
    btn.addEventListener('click', () => {
        delRow(btn)
    })
})

addRowBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        addTableRow()
    })
})


function getData(data) {
    return JSON.parse(data)
}


function addTableRow() {
    // console.log(accounts)
    // console.log(categories)
    let addExpenseTable = document.querySelector("#addExpensesTable")
    let addExpenseTableBody = document.querySelector("#addExpensesTableBody")

    // console.log(addExpenseTableBody.rows.item(addExpenseTableBody.rows.length - 1))
    // console.log(parseInt(addExpenseTableBody.rows.item(addExpenseTableBody.rows.length - 1).firstElementChild.textContent) + 1)
    let newRow = addExpenseTable.insertRow(-1)
    let orderNumber = newRow.insertCell(0)

    // orderNumber.innerHTML = parseInt(addExpenseTableBody.rows.item(addExpenseTableBody.rows.length - 1).firstElementChild.textContent) + 1
    orderNumber.innerHTML = 0
    orderNumber.classList.add('align-middle')


    let cell2 = newRow.insertCell(1)
    cell2.innerHTML = `<input type="text" name="amount" placeholder="0" 
    pattern="^(([1-9]\\d{0,2}(\\d{3})*)|\\d+)?(,\\d{1,2})?$"
    title="Podaj wartość całkowitą, lub po przecinku np. 0,25, 30, 21,3"
    class="form-control" required>`

    let cell3 = newRow.insertCell(2)
    cell3.innerHTML = `<input type="text" name="description" pattern="^(\\S| ){1,100}$" title="Opis nie może być pusty i może zawierać maksymalnie 100 znaków" class="form-control">`

    let categorySelect = `<select class="form-select" aria-label="Category" name="category">`
    categories.forEach(category => {
        categorySelect += `<option value="${category._id.$oid}">${category.name}</option>`
    })
    categorySelect += `</select>`

    let cell4 = newRow.insertCell(3)
    cell4.innerHTML = categorySelect
    
    let accountSelect = `<select class="form-select" aria-label="Account" name="account">`
    accounts.forEach(account => {
        accountSelect += `<option value="${account._id.$oid}">${account.name}</option>`
    })
    accountSelect += `</select>`


    let cell5 = newRow.insertCell(4)
    cell5.innerHTML = accountSelect

    let cell6 = newRow.insertCell(5)
    cell6.innerHTML = `<input type="date" name="date" value="${dateNow}" class="form-control" required>`

    let cell7 = newRow.insertCell(6)
    cell7.innerHTML = `<button type="button" class="btn btn-close btnDelRow"></button>`
    cell7.classList.add('align-middle')
    
    let btn = cell7.firstElementChild


    btn.addEventListener('click', () => {
        delRow(btn)
    })
    
    rowCount = countRows()
    refreshTable(rowCount)
}

function delRow(btn) {
    let row = btn.parentNode.parentNode
    let tbody = btn.parentNode.parentNode.parentNode
    tbody.removeChild(row)

    rowCount = countRows()
    refreshTable(rowCount)
}

function refreshTable(rowCount) {
    let addExpenseTableBody = document.querySelector("#addExpensesTableBody")

    for (let i = 0; i < rowCount; i++) {
        addExpenseTableBody.children[i].children[0].innerHTML = String(i + 1)
    }
}

function countRows() {
    let addExpenseTableBody = document.querySelector("#addExpensesTableBody")
    let rows = addExpenseTableBody.children.length
    return rows
}
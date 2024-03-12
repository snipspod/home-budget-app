const includeSwitches = document.querySelectorAll('.form-check-input')
const percentageFields = document.querySelectorAll('.percentage-group')
const budgetBtn = document.querySelector('#add-budget-btn')
const modalDelete = document.getElementById('modalDelete')
const modalUpdate = document.getElementById('modalUpdate')

function getData(data) {
    return JSON.parse(data)
}

if (modalDelete) {
    modalDelete.addEventListener('show.bs.modal', event => {
        const btn = event.relatedTarget
        const budgetId = btn.dataset.budget
        const budgetName = modalDelete.querySelector('.modal-body h5 span')
        const budgetIdModal = modalDelete.querySelector('#budget_id')
        const budgets = getData(_budgets)

        let currentBudgetData = budgets.find(({ _id }) => _id.$oid == budgetId)

        budgetName.innerText = currentBudgetData.name
        budgetIdModal.value = budgetId
    })
}

if (modalUpdate) {
    modalUpdate.addEventListener('show.bs.modal', event => {
        const btn = event.relatedTarget
        const budgetId = btn.dataset.budget
        const budgetAmount = btn.dataset.amount
        const bdugetMonth= btn.dataset.month
        const budgetNameModal = modalDelete.querySelector('#new_budget_name')
        console.log(budgetNameModal)
        const budgetIdModal = modalDelete.querySelector('#budget_id')
        const budgetMonthModal = modalDelete.querySelector('#new_budget_month')
        const budgets = getData(_budgets)

        currentBudgetData = budgets.find(({ _id }) => _id.$oid == budgetId)
        budgetIdModal.value = budgetId
        budgetNameModal.value = currentBudgetData.name

    })
}

let totalSum = 0

percentageFields.forEach(field => {
    field.addEventListener('input', event => {

        let totalSum = 0
    
        includeSwitches.forEach(element => {
            if (element.checked) {
                let percentageField = document.querySelector(`#${element.id.replace('include_', 'percentage_')}`)
                totalSum += parseInt(percentageField.value)
            }
        })
        if (totalSum == 100 ) {
            console.log('true')
            budgetBtn.disabled = false
        } else {
            console.log('false')
            budgetBtn.disabled = true
        }
    })
})
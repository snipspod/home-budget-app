const includeSwitches = document.querySelectorAll('.form-check-input')
const percentageFields = document.querySelectorAll('.percentage-group')
const budgetBtn = document.querySelector('#add-budget-btn')
const modalDelete = document.getElementById('modalDelete')
const modalUpdate = document.getElementById('modalUpdate')


if (modalDelete) {
    modalDelete.addEventListener('show.bs.modal', event => {
        const btn = event.relatedTarget
        const budgetName = modalDelete.querySelector('.modal-body h5 span')
        const budgetIdModal = modalDelete.querySelector('#budget_id')

        budgetName.innerText = btn.dataset.name
        budgetIdModal.value = btn.dataset.budget
    })
}

if (modalUpdate) {
    modalUpdate.addEventListener('show.bs.modal', event => {
        const btn = event.relatedTarget
        const budgetNameModal = modalUpdate.querySelector('#new_budget_name')
        const budgetIdModal = modalUpdate.querySelector('#budget_id')
        const budgetMonthModal = modalUpdate.querySelector('#new_budget_month')
        const budgetAmountModal = modalUpdate.querySelector('#new_budget_amount')
        const budgetCategoriesModal = modalUpdate.querySelector('#new_budget_categories')
        const categories = JSON.parse(_categories)
        const assoc_categories = JSON.parse(btn.dataset.categories.replaceAll("'",'"'))

        budgetIdModal.value = btn.dataset.budgetid
        budgetNameModal.value = btn.dataset.name
        budgetMonthModal.value = btn.dataset.month
        budgetAmountModal.value = btn.dataset.amount.replace('.', ',')

        categories.forEach((category) => {
            accordion_start = `<div class="col-4"><div class="d-flex accordion justify-content-center flex-column mb-3"><p class="fs-5 mb-1 mx-auto">${category.name}</p><div class="form-check form-switch mb-3 mx-auto">`
        
            if (found_category = assoc_categories.find(({category_id}) => category_id.$oid == category._id.$oid)){
                accordion_end = `<input type="checkbox" class="form-check-input" role="switch" name="include_${category._id.$oid}" id="include_${category._id.$oid}" form="update_budget" data-bs-toggle="collapse" data-bs-target="#accordion_${category._id.$oid}" aria-controls="accordion_${category._id.$oid}" checked></div><div class="accordion-collapse collapse text-center show" id="accordion_${category._id.$oid}"><p class="mb-2">Procent budżetu do przeznaczenia</p><div class="input-group mx-auto w-75"><input type="number" min="1" max="100" form="update_budget" name="percentage_${category._id.$oid}" id="percentage_${category._id.$oid}" class="form-control w-50 rounded-start percentage-group" aria-label="Dolar amount" value="${Math.round((found_category.amount/btn.dataset.amount)*100)}"><span class="input-group-text">%</span></div></div></div></div>`
            } else {
                accordion_end = `<input type="checkbox" class="form-check-input" role="switch" name="include_${category._id.$oid}" id="include_${category._id.$oid}" form="update_budget" data-bs-toggle="collapse" data-bs-target="#accordion_${category._id.$oid}" aria-controls="accordion_${category._id.$oid}"></div><div class="accordion-collapse collapse text-center" id="accordion_${category._id.$oid}"><p class="mb-2">Procent budżetu do przeznaczenia</p><div class="input-group mx-auto w-75"><input type="number" min="1" max="100" form="update_budget" name="percentage_${category._id.$oid}" id="percentage_${category._id.$oid}" class="form-control w-50 rounded-start percentage-group" aria-label="Dolar amount"><span class="input-group-text">%</span></div></div></div></div>`
            }

            accordion = accordion_start + accordion_end
            budgetCategoriesModal.innerHTML += accordion
            // console.log(accordion)
        })
        


    })

    modalUpdate.addEventListener('hidden.bs.modal', (event) => {
        const budgetCategoriesModal = modalUpdate.querySelector('#new_budget_categories')
        budgetCategoriesModal.innerHTML = ''
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
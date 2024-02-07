const includeSwitches = document.querySelectorAll('.form-check-input')
const percentageFields = document.querySelectorAll('.percentage-group')
const budgetBtn = document.querySelector('#add-budget-btn')

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
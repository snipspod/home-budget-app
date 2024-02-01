const modalDelete = document.getElementById('modalDelete')
const modalUpdate = document.getElementById('modalUpdate')
const modalAdd = document.getElementById('modalAdd')

function getData(data) {
  return JSON.parse(data)
}


if (modalDelete) {
  modalDelete.addEventListener('show.bs.modal', event => {
    const btn = event.relatedTarget
    console.log(btn)
    const account = btn.dataset.account
    const accountName = modalDelete.querySelector('.modal-body h5 span')
    const accountField = modalDelete.querySelector('#account')

    accountName.innerText = account
    accountField.value = account
  })
}

if (modalUpdate) {
    modalUpdate.addEventListener('show.bs.modal', event => {
        const btn = event.relatedTarget
        const current_account = btn.dataset.account
        const current_balance = btn.dataset.balance.replace('.', ',')
        const oldAccountName = modalUpdate.querySelector('#old_account_name')
        const accountName = modalUpdate.querySelector('#new_account_name')
        const accountBalance = modalUpdate.querySelector('#balance_new')
        const cyclicalCheck = modalUpdate.querySelector('#is_cyclical')
        const cyclicalAccordion = modalUpdate.querySelector('#cyclical')
        const cyclicalAmount = modalUpdate.querySelector('#income_amount')
        const cyclicalDay = modalUpdate.querySelector('#income_day')
        const accounts = getData(_accounts)

        currentAccountData = accounts.find(({ name }) => name == current_account)
        if (currentAccountData.income_active) {
          cyclicalCheck.checked = true
          cyclicalAccordion.classList.add('show')
          cyclicalAmount.value = currentAccountData.income
          cyclicalDay.value = currentAccountData.income_day
        } else {
          cyclicalCheck.checked = false
          cyclicalAccordion.classList.remove('show')
          cyclicalAmount.value = '0'
          cyclicalDay.value = 1
        }

        cyclicalCheck.addEventListener('change', () => {
          if(!cyclicalAmount.required) {
            cyclicalAmount.required = true
          } else if (cyclicalAmount.required) {
            cyclicalAmount.required = false
          }
        })
        accountName.value = current_account
        accountBalance.value = current_balance
        oldAccountName.value = current_account

    })
}

if (modalAdd) {
  modalAdd.addEventListener('show.bs.modal', event => {
      const cyclicalCheck = modalAdd.querySelector('#is_cyclical')
      const cyclicalAmount = modalAdd.querySelector('#income_amount')

      cyclicalCheck.addEventListener('change', () => {
        if(!cyclicalAmount.required) {
          cyclicalAmount.required = true
        } else if (cyclicalAmount.required) {
          cyclicalAmount.required = false
        }
      })
  })
}
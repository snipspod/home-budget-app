const modalDelete = document.getElementById('modalDelete')
const modalUpdate = document.getElementById('modalUpdate')

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
        const accountName = modalUpdate.querySelector('#account_new')
        const accountBalance = modalUpdate.querySelector('#balance_new')

        accountName.value = current_account
        accountBalance.value = current_balance

    })
}
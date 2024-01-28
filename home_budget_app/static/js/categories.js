const modalDelete = document.getElementById('modalDelete')
if (modalDelete) {
  modalDelete.addEventListener('show.bs.modal', event => {
    const btn = event.relatedTarget
    const category = btn.getAttribute('data-bs-category')
    const categoryModal = modalDelete.querySelector('.modal-body h5 span')
    const categoryField = modalDelete.querySelector('#category')

    categoryModal.innerText = category
    categoryField.value = category
  })
}

const modalUpdate = document.getElementById('modalUpdate')

if(modalUpdate) {
  modalUpdate.addEventListener('show.bs.modal', event => {
    const btn = event.relatedTarget
    const category = btn.getAttribute('data-bs-category')
    const category_old = modalUpdate.querySelector('#category_old')
    const category_new = modalUpdate.querySelector('#category_new')

    category_old.value = category
    category_new.placeholder = category
  })
}
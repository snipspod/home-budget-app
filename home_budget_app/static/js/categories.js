const modalDelete = document.getElementById('modalDelete')
if (modalDelete) {
  modalDelete.addEventListener('show.bs.modal', event => {
    const btn = event.relatedTarget
    const category = JSON.parse(btn.getAttribute('data-bs-category').replaceAll("'", '"'))
    const categoryModal = modalDelete.querySelector('.modal-body h5 span')
    const categoryId = modalDelete.querySelector('#category_id')

    categoryModal.innerText = category.name
    categoryId.value = category._id.$oid
  })
}

const modalUpdate = document.getElementById('modalUpdate')

if(modalUpdate) {
  modalUpdate.addEventListener('show.bs.modal', event => {
    const btn = event.relatedTarget
    const category = JSON.parse(btn.getAttribute('data-bs-category').replaceAll("'", '"'))
    const categoryId = modalUpdate.querySelector('#category_id')
    const categoryName = modalUpdate.querySelector('#category_new')

    console.log(category._id.$oid)

    categoryId.value = category._id.$oid
    categoryName.placeholder = category.name
  })
}
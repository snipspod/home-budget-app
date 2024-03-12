const toastLiveExample = document.getElementById('liveToast')
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
const navbarCollapse = document.querySelector('#navbarSideCollapse')
const accountDropdown = document.querySelector('#account-dropdown')

if (toastBootstrap._element != null) {
    toastBootstrap.show()
}

// navbarCollapse.addEventListener('click', () => {
//     document.querySelector('.offcanvas-collapse').classList.toggle('open')
//   })

navbarCollapse.addEventListener('click', () => {
    document.querySelector('.offcanvas-collapse').classList.toggle('open')
})

window.addEventListener('resize', () => {
    if (window.innerWidth < 992) {
        accountDropdown.classList.remove('dropstart')
        accountDropdown.classList.add('dropdown')
    } else {
        accountDropdown.classList.remove('dropdown')
        accountDropdown.classList.add('dropstart')
    }
})
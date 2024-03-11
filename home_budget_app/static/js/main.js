let toastLiveExample = document.getElementById('liveToast')
let toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
let navbarCollapse = document.querySelector('#navbarSideCollapse')

if (toastBootstrap._element != null) {
    toastBootstrap.show()
}

// navbarCollapse.addEventListener('click', () => {
//     document.querySelector('.offcanvas-collapse').classList.toggle('open')
//   })

navbarCollapse.addEventListener('click', () => {
    document.querySelector('.offcanvas-collapse').classList.toggle('open')
})
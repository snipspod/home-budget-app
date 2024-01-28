let toastLiveExample = document.getElementById('liveToast')
let toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

if (toastBootstrap._element != null) {
    toastBootstrap.show()
}
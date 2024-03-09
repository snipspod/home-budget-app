const passwordField = document.querySelector('#password')
const passwordConfirmField = document.querySelector('#password_confirm')
const registerButton = document.querySelector('#register_button')
const passwordsInfo = document.querySelector('#passwords_match_info')

const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+[{\]}\\\|;:'",<.>\/\?`~])[A-Za-z\d!@#$%^&*()-_=+[{\]}\\\|;:'",<.>\/\?`~]{8,50}$/

let passwordMatchesRegex = false

passwordField.addEventListener('input', event => {
    if (passwordRegex.test(passwordField.value)) {
        passwordMatchesRegex = true
    }
})

passwordConfirmField.addEventListener('input', event => {
    if (passwordField.value == passwordConfirmField.value && passwordMatchesRegex) {
        registerButton.disabled = false
        passwordsInfo.classList.remove('d-none')
    } else {
        registerButton.disabled = true
        passwordsInfo.classList.add('d-none')
    }
})
const oldPasswordField = document.querySelector('#old_password')
const newPasswordField = document.querySelector('#new_password')
const confirmNewPasswordField = document.querySelector('#new_password_confirm')
const deletePassword = document.querySelector('#password')
const deletePasswordConfirm = document.querySelector('#password_confirm')
const changePasswordButton = document.querySelector('#change_password_button')
const deleteAccountButton = document.querySelector('#delete_account_button')

const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+[{\]}\\\|;:'",<.>\/\?`~])[A-Za-z\d!@#$%^&*()-_=+[{\]}\\\|;:'",<.>\/\?`~]{8,50}$/

let passwordChangeMatchesRegex = false
let passwordDeleteMatchesRegex = false

newPasswordField.addEventListener('input', event => {
    if (passwordRegex.test(newPasswordField.value)) {
        passwordChangeMatchesRegex = true
    }
})

confirmNewPasswordField.addEventListener('input', event => {
    if (newPasswordField.value == confirmNewPasswordField.value && passwordChangeMatchesRegex) {
        changePasswordButton.disabled = false
    } else {
        changePasswordButton.disabled = true
    }
})

deletePassword.addEventListener('input', event => {
    if (passwordRegex.test(deletePassword.value)) {
        passwordDeleteMatchesRegex = true
    }
})

deletePasswordConfirm.addEventListener('input', event => {
    if (deletePassword.value == deletePasswordConfirm.value && passwordDeleteMatchesRegex) {
        deleteAccountButton.disabled = false
    } else {
        deleteAccountButton.disabled = true
    }
})
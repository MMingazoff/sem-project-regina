function checkRegForm(event) {
    let first_name = document.getElementById("first_name")
    let last_name = document.getElementById("last_name")
    let email = document.getElementById("email")
    let phone_num = document.getElementById("phone_num")
    let password = document.getElementById("password")
    let conf_password = document.getElementById("conf_password")
    if ((first_name.value === '') || (last_name.value === '') || (email.value === '') || (phone_num.value === '') || (password.value === '') || (conf_password.value === '')) {
        window.alert('Some field is empty')
        event.preventDefault()
    } else if (password.value !== conf_password.value) {
        window.alert('Password not exist')
        event.preventDefault()
    }
}

function checkLogForm(event) {
    let email = document.getElementById("email")
    let phone_num = document.getElementById("phone_num")
    let password = document.getElementById("password")
    if ((email.value === '') || (password.value === '') || (phone_num.value === '')) {
        window.alert('Some field is empty')
        event.preventDefault()
    }
}
function checkDelete(id) {
  let text = "Confirm delete product";
  if (confirm(text)) {
      window.location.replace('/product/' + id + '/delete')
  }
}
function makeInvalid(elem_feedback, input_elem, msg) {
    elem_feedback.innerHTML = msg
    input_elem.classList.add('is-invalid')
    // elem_feedback.style.display = 'block'

}

function removeIsInvalidClass(elem) {

    document.querySelectorAll('.invalid-feedback').forEach((e) => {e.innerHTML = 'Required field'})

    console.log(elem)

    elem.classList.remove('was-validated')
    
    let children = elem.querySelectorAll('*');

    for (let child of children) {
        child.classList.remove('is-invalid');
    }
}

let forms = document.querySelectorAll('.needs-validation') 

for (let form of forms) {
    form.addEventListener('submit', async function(event) {

        removeIsInvalidClass(event.target)
        

        let is_login = false;
        
        if (this.id === 'login-form') {
            is_login = true
        }

        if (!form.checkValidity()) {

            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
            return;
        }

        event.preventDefault();

        let formData = new FormData(this); 
        console.log(formData)

    try {   
        let action = '/login'

        if (!is_login) {
            action = '/register'

        }
        console.log(action)
        const response = await fetch(action, { method: "POST", body: formData});

        const data = await response.json(); // Parse response JSON

        console.log("hahaha")

        if (data['success'] == true) {
            console.log("success!!")

            if (is_login) window.location.href = '/dashboard';
            else {
                $('#registerModal').on('hidden.bs.modal', function () {
                    $(this).find('form').trigger('reset');
                });
                $('#registerModal').modal('hide');
                //window.location.href = '/';
                $('#loginModal').modal('show');

            }
            return
        }
        else {
            console.log('AHAHAH')

            if (data.hasOwnProperty('regex-error')){
                msg = data['msg']
                if (data['regex-error'] === 'username') {
                    console.log("here")
                    if (is_login){
                        makeInvalid(document.getElementById('login-username-error'), document.getElementById('username-login'), msg)
                        
                    }
                    else {
                        makeInvalid(document.getElementById('register-username-error'),document.getElementById('username-register'), msg)
                    }
                }
                else {
                    if (is_login) {
                        makeInvalid(document.getElementById('login-password-error'), document.getElementById('password-login'),msg)
                    }
                    else {
                        makeInvalid(document.getElementById('register-password-error'), document.getElementById('passowrd-register'),msg)
                    }
                }
                return
                
            }

            if (data.hasOwnProperty('user-exists')) {
                msg = data['msg']

                console.log(msg)
                if (data['user-exists']) {
                    makeInvalid(document.getElementById('register-username-error'), document.getElementById('username-register'),msg)

                }
                else makeInvalid(document.getElementById('login-username-error'), document.getElementById('username-login'),msg)

                return 
            }
            else if (data.hasOwnProperty('incorrect-password')) {
                msg = data['msg']
                makeInvalid(document.getElementById('login-password-error'), document.getElementById('password-login'),msg)
                return
            }

            
            if (data.hasOwnProperty('non-matching-passwords')) {
                msg = data['msg']
                makeInvalid(document.getElementById('register-password-confirm-error'), document.getElementById('password-confirm-register'), msg)

            }

            // if (data.hasOwnProperty('redirect')) window.location.href = data.redirect;

        }

    } catch (error) {
        console.error('Some network error occured', error);
    }

    })
}
let id = (id) => document.getElementById(id);
let classes = (classes) => document.getElementsByClassName(classes);

let username = id("username"),
    email = id("email"),
    password = id("password"),
    form = id("form");

let errorMsg = classes("error"),
    successIcon = classes("succes-icon"), // Обратите внимание: 'succes' без второй 's'
    failureIcon = classes("failure-icon");

// Проверка пароля и обновление иконок
function checkPassword(pass) {
    const checks = {
        lowercase: /[a-z]/.test(pass),
        uppercase: /[A-Z]/.test(pass),
        number: /\d/.test(pass),
        length: pass.length >= 8
    };
    
    // Обновляем иконки в списке
    const items = document.querySelectorAll('.requirement-item');
    items.forEach((item, i) => {
        const icon = item.querySelector('i');
        const isValid = Object.values(checks)[i];
        
        if (isValid) {
            icon.className = 'fas fa-check-circle';
            icon.style.color = '#00c851';
        } else {
            icon.className = 'fas fa-times-circle';
            icon.style.color = '#ff4444';
        }
    });
    
    // Все проверки пройдены?
    return Object.values(checks).every(check => check === true);
}

// Сброс иконок пароля
function resetPasswordIcons() {
    const icons = document.querySelectorAll('.requirement-item i');
    icons.forEach(icon => {
        icon.className = 'fa-solid fa-circle';
        icon.style.color = '#888';
    });
}

// Проверка поля формы
function validateField(field, index, message) {
    const value = field.value.trim();
    
    if (value === "") {
        errorMsg[index].innerHTML = message;
        field.style.border = "2px solid red";
        successIcon[index].style.opacity = "0";
        failureIcon[index].style.opacity = "1";
        return false;
    }
    
    // Для пароля проверяем требования
    if (field === password && !checkPassword(value)) {
        errorMsg[index].innerHTML = "Пароль не соответствует требованиям";
        field.style.border = "2px solid red";
        successIcon[index].style.opacity = "0";
        failureIcon[index].style.opacity = "1";
        return false;
    }
    
    errorMsg[index].innerHTML = "";
    field.style.border = "2px solid green";
    successIcon[index].style.opacity = "1";
    failureIcon[index].style.opacity = "0";
    return true;
}

// Валидация пароля при вводе
if (password) {
    password.addEventListener('input', function() {
        if (this.value.length > 0) {
            checkPassword(this.value);
        } else {
            resetPasswordIcons();
        }
    });
}

// Отправка формы
if (form) {
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const validUsername = validateField(username, 0, "Username cannot be blank");
        const validEmail = validateField(email, 1, "Email cannot be blank");
        const validPassword = validateField(password, 2, "Password cannot be blank");
        
        if (validUsername && validEmail && validPassword) {
            alert("Форма успешно отправлена!");
            form.reset();
            resetPasswordIcons();
        }
    });
}
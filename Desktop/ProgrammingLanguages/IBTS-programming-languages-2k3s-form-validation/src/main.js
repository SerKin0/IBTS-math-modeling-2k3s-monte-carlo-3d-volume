let id = (id) => document.getElementById(id);
let classes = (classes) => document.getElementsByClassName(classes);

let username = id("username"),
    email = id("email"),
    password = id("password"),
    form = id("form");

let errorMsg = classes("error"),
    successIcon = classes("success-icon"),
    failureIcon = classes("failure-icon");

// Функция проверки пароля и обновления списка требований
function checkPassword(pass) {
    const checks = {
        lowercase: /[a-z]/.test(pass),
        uppercase: /[A-Z]/.test(pass),
        number: /\d/.test(pass),
        length: pass.length >= 8
    };

    document.querySelectorAll('.requirement-item').forEach(item => {
        const req = item.getAttribute('data-requirement');
        const icon = item.querySelector('.requirement-icon');
        if (checks[req]) {
            icon.classList.add('valid');
            icon.classList.remove('invalid');
        } else {
            icon.classList.add('invalid');
            icon.classList.remove('valid');
        }
    });

    return Object.values(checks).every(v => v);
}

// Сброс иконок требований пароля
function resetPasswordIcons() {
    document.querySelectorAll('.requirement-icon').forEach(icon => {
        icon.classList.remove('valid', 'invalid');
    });
}

// Универсальная функция проверки одного поля в реальном времени
function validateFieldLive(field, index, emptyMsg) {
    const value = field.value.trim();

    // Если поле пустое — показываем ничего (или можно failure, но по заданию — только при ошибке)
    if (value === "") {
        errorMsg[index].textContent = "";
        field.style.border = "2px solid #c4c4c4";
        successIcon[index].style.opacity = "0";
        failureIcon[index].style.opacity = "0";
        return;
    }

    let isValid = true;

    // Специальная проверка для email (простая, но достаточная)
    if (field === email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        isValid = emailRegex.test(value);
        if (!isValid) {
            errorMsg[index].textContent = "Email is not valid";
        }
    }

    // Специальная проверка для пароля
    if (field === password) {
        isValid = checkPassword(value);
        if (!isValid && value.length > 0) {
            errorMsg[index].textContent = "Password does not meet requirements";
        }
    }

    // Для username — просто непустое
    if (field === username && value.length < 3) {
        isValid = false;
        errorMsg[index].textContent = "Username must be at least 3 characters";
    }

    // Применяем стили и иконки
    if (isValid) {
        errorMsg[index].textContent = "";
        field.style.border = "2px solid green";
        successIcon[index].style.opacity = "1";
        failureIcon[index].style.opacity = "0";
    } else {
        if (value !== "") { // Показываем ошибку только если поле не пустое
            field.style.border = "2px solid red";
            successIcon[index].style.opacity = "0";
            failureIcon[index].style.opacity = "1";
        }
    }
}

// Очистка стилей при фокусе (опционально — красиво)
function clearFieldStyles(field, index) {
    field.style.border = "2px solid #f2796e"; // фокус-цвет
    errorMsg[index].textContent = "";
    successIcon[index].style.opacity = "0";
    failureIcon[index].style.opacity = "0";
}

// Добавляем обработчики ввода для каждого поля
username.addEventListener('input', () => validateFieldLive(username, 0, "Username cannot be blank"));
email.addEventListener('input', () => validateFieldLive(email, 1, "Email cannot be blank"));
password.addEventListener('input', () => validateFieldLive(password, 2, "Password cannot be blank"));

// При фокусе — подсвечиваем и убираем ошибки
username.addEventListener('focus', () => clearFieldStyles(username, 0));
email.addEventListener('focus', () => clearFieldStyles(email, 1));
password.addEventListener('focus', () => clearFieldStyles(password, 2));

// При потере фокуса — можно проверить снова (если нужно)
username.addEventListener('blur', () => validateFieldLive(username, 0));
email.addEventListener('blur', () => validateFieldLive(email, 1));
password.addEventListener('blur', () => validateFieldLive(password, 2));

// Сброс при очистке формы
form.addEventListener("reset", () => {
    setTimeout(() => { // небольшой таймаут, чтобы сработало после reset
        username.style.border = email.style.border = password.style.border = "2px solid #c4c4c4";
        errorMsg[0].textContent = errorMsg[1].textContent = errorMsg[2].textContent = "";
        successIcon.forEach(icon => icon.style.opacity = "0");
        failureIcon.forEach(icon => icon.style.opacity = "0");
        resetPasswordIcons();
    }, 10);
});

form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Проверяем все поля в реальном времени
    validateFieldLive(username, 0);
    validateFieldLive(email, 1);
    validateFieldLive(password, 2);

    const usernameValid = username.value.trim() !== "" && username.value.trim().length >= 3;
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
    const passwordValid = checkPassword(password.value);

    if (usernameValid && emailValid && passwordValid) {
        // Сохраняем данные в localStorage
        localStorage.setItem("reg_username", username.value.trim());
        localStorage.setItem("reg_email", email.value.trim());

        // Отправляем письмо
        sendMail();

        // Переходим на страницу успеха
        window.location.href = "templates/success.html";
    } else {
        alert("Пожалуйста, исправьте ошибки в форме.");
    }
});
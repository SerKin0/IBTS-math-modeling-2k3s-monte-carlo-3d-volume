function sendMail() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value; // можно не показывать, но если нужно — оставь

    // Формируем тело письма
    const body = `
Новое регистрационное сообщение:

Имя пользователя: ${username}
Email: ${email}
Дата регистрации: ${new Date().toLocaleString('ru-RU')}
    `.trim();

    // Кодируем для URL
    const encodedBody = encodeURIComponent(body);

    // Открываем почтовый клиент
    window.location.href = `mailto:rfunn2021@gmail.com?subject=New Registration - Happy New Year&body=${encodedBody}`;
}
function sendMail() {
    // Получаем данные из формы
    const username = document.getElementById("username").value || "";
    const email = document.getElementById("email").value || "";
    
    // Создаем текст письма
    const body = `Имя: ${username}%0D%0AEmail: ${email}`;
    
    // Открываем почтовый клиент
    window.location.href = "mailto:sergey.skor007@gmail.com?subject=Happy New Year&body=" + body;
}
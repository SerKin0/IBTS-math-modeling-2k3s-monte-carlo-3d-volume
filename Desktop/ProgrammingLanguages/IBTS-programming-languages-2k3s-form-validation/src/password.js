const passwordInput = document.getElementById("password");
const eyeIcon = document.getElementById("togglePassword");

if (passwordInput && eyeIcon) 
{
    eyeIcon.addEventListener("click", () => {
        const typeInputPlace = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", typeInputPlace);
        eyeIcon.classList.toggle("fa-eye");
        eyeIcon.classList.toggle("fa-eye-slash");
    });
}

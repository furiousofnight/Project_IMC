// Funções interativas opcionais
document.addEventListener("DOMContentLoaded", function () {
    const errorElement = document.querySelector(".error");
    if (errorElement) {
        // Remover a mensagem de erro após 5 segundos
        setTimeout(() => {
            errorElement.style.display = "none";
        }, 5000);
    }
});
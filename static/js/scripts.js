// Funções interativas e animações
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitButton = document.querySelector("button[type='submit']");
    const inputs = document.querySelectorAll("input[required], select[required]");

    // Atualização do token CSRF
    function updateCSRFToken() {
        fetch('/get_csrf_token')
            .then(response => response.json())
            .then(data => {
                document.querySelector('input[name="csrf_token"]').value = data.csrf_token;
            })
            .catch(error => console.error('Erro ao atualizar token CSRF:', error));
    }

    // Atualizar token CSRF a cada 30 minutos
    setInterval(updateCSRFToken, 30 * 60 * 1000);

    // Gerenciamento de mensagens de erro
    const errorElement = document.querySelector(".error");
    if (errorElement) {
        // Adiciona classe para animar a entrada da mensagem
        errorElement.classList.add("fadeIn");
        
        // Remove a mensagem de erro com animação após 5 segundos
        setTimeout(() => {
            errorElement.classList.add("fadeOut");
            setTimeout(() => {
                errorElement.style.display = "none";
            }, 500); // Tempo da animação de fade out
        }, 5000);
    }

    // Validação em tempo real dos campos
    inputs.forEach(input => {
        // Adiciona classe de animação no foco
        input.addEventListener("focus", function() {
            this.closest(".form-group").classList.add("input-focused");
        });

        // Remove classe de animação quando perde foco
        input.addEventListener("blur", function() {
            if (!this.value) {
                this.closest(".form-group").classList.remove("input-focused");
            }
            validateInput(this);
        });

        // Validação em tempo real para campos numéricos
        if (input.type === "number") {
            input.addEventListener("input", function() {
                const value = parseFloat(this.value);
                
                if (this.id === "idade") {
                    if (value < 1 || value > 120) {
                        showInputError(this, "A idade deve estar entre 1 e 120 anos");
                    } else {
                        clearInputError(this);
                    }
                } else if (this.id === "peso") {
                    if (value < 1 || value > 300) {
                        showInputError(this, "O peso deve estar entre 1 e 300 kg");
                    } else {
                        clearInputError(this);
                    }
                } else if (this.id === "altura") {
                    if (value < 0.5 || value > 3) {
                        showInputError(this, "A altura deve estar entre 0.5 e 3 metros");
                    } else {
                        clearInputError(this);
                    }
                }
            });
        }
    });

    // Função para mostrar erro no campo
    function showInputError(input, message) {
        const formGroup = input.closest(".form-group");
        let errorDiv = formGroup.querySelector(".input-error-message");
        
        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.className = "input-error-message";
            formGroup.appendChild(errorDiv);
        }
        
        input.classList.add("is-invalid");
        errorDiv.textContent = message;
        errorDiv.style.display = "block";
    }

    // Função para limpar erro do campo
    function clearInputError(input) {
        const formGroup = input.closest(".form-group");
        const errorDiv = formGroup.querySelector(".input-error-message");
        
        input.classList.remove("is-invalid");
        if (errorDiv) {
            errorDiv.style.display = "none";
        }
    }

    // Função para validar um campo específico
    function validateInput(input) {
        if (!input.value.trim()) {
            showInputError(input, "Este campo é obrigatório");
            return false;
        }
        
        if (input.type === "number") {
            const value = parseFloat(input.value);
            if (isNaN(value)) {
                showInputError(input, "Digite um número válido");
                return false;
            }
        }
        
        clearInputError(input);
        return true;
    }

    // Validação do formulário completo
    function validateForm() {
        let isValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });
        return isValid;
    }

    // Função para mostrar mensagens toast
    function showToast(message, type = 'error') {
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add("show");
            setTimeout(() => {
                toast.classList.remove("show");
                setTimeout(() => document.body.removeChild(toast), 300);
            }, 3000);
        });
    }

    // Envio do formulário
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            
            if (!validateForm()) {
                showToast("Por favor, preencha todos os campos corretamente");
                return;
            }

            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculando...';

            // Enviar formulário
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro no servidor');
                }
                return response.text();
            })
            .then(html => {
                // Redirecionar para a página de resultados
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => {
                console.error('Erro:', error);
                showToast("Ocorreu um erro. Por favor, tente novamente.");
                submitButton.disabled = false;
                submitButton.innerHTML = '<i class="fas fa-calculator"></i> Calcular';
            });
        });
    }

    // Animações de entrada
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    animateElements.forEach(element => observer.observe(element));
});
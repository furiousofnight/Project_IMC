document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.querySelector('.progress-bar-imc');
    if (progressBar) {
        const progress = progressBar.getAttribute('data-progress');
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('role', 'progressbar');
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.setAttribute('aria-valuemin', '0');
        progressBar.setAttribute('aria-valuemax', '100');
    }

    // Animação de entrada dos elementos
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });

    // Adicionar animação de hover aos cartões métricos
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        card.classList.add('hover-effect');
    });

    // Adicionar tooltips aos valores de resultado
    const resultValues = document.querySelectorAll('.result-value');
    resultValues.forEach(value => {
        value.setAttribute('title', 'Clique para copiar');
        value.style.cursor = 'pointer';
        
        value.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                showToast('Valor copiado para a área de transferência!');
            }).catch(() => {
                showToast('Não foi possível copiar o valor');
            });
        });
    });

    // Botão de retorno
    const returnButton = document.querySelector('.btn-primary');
    returnButton.addEventListener('click', () => {
        document.body.style.opacity = '0';
        setTimeout(() => {
            window.location.href = '/';
        }, 300);
    });

    // Animação de scroll suave para recomendações
    const recommendationBox = document.querySelector('.recommendation-box');
    if (recommendationBox) {
        setTimeout(() => {
            recommendationBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 1000);
    }

    // Animação ao rolar
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

    animateElements.forEach(element => {
        observer.observe(element);
    });

    // Animação da barra de progresso
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        setTimeout(() => {
            progressBar.style.width = progressBar.getAttribute('aria-valuenow') + '%';
        }, 500);
    }

    // Imprimir resultados
    document.querySelector('.btn-secondary')?.addEventListener('click', function(e) {
        e.preventDefault();
        window.print();
    });
});

// Função para exibir toast de notificação
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    
    setTimeout(() => {
        toast.className = toast.className.replace('show', '');
    }, 3000);
}

// Função para animar elementos quando eles entram na viewport
function handleScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(element => {
        observer.observe(element);
    });
}

// Função para voltar para a página inicial
function voltarParaInicio() {
    window.location.href = '/';
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    handleScrollAnimations();
}); 
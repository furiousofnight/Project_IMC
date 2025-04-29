class AudioManager {
    constructor() {
        // Inicializar variáveis de áudio
        this.backgroundMusic = new Audio('/static/audio/background.mp3');
        this.clickSound = new Audio('/static/audio/click.mp3');
        
        // Configurar música de fundo
        this.backgroundMusic.loop = true;
        this.backgroundMusic.volume = 0.3;
        
        // Configurar som de clique
        this.clickSound.volume = 0.5;
        
        // Estado do áudio
        this.isMuted = false;
        this.musicPlaying = false;
        this.isClickReady = true;
        this.clickQueue = [];
        
        // Carregar preferências do usuário
        this.loadPreferences();
        
        // Configurar intervalo para processar a fila de cliques
        setInterval(() => this.processClickQueue(), 2000);
    }
    
    loadPreferences() {
        const muted = localStorage.getItem('audioMuted');
        if (muted === 'true') {
            this.muteAll();
        }
    }
    
    async playBackgroundMusic() {
        if (!this.musicPlaying && !this.isMuted) {
            try {
                // Delay inicial de 2 segundos antes de começar a música
                await new Promise(resolve => setTimeout(resolve, 2000));
                await this.backgroundMusic.play();
                this.musicPlaying = true;
                
                // Configurar fade in
                let volume = 0;
                const fadeInterval = setInterval(() => {
                    if (volume < 0.3) {
                        volume += 0.01;
                        this.backgroundMusic.volume = volume;
                    } else {
                        clearInterval(fadeInterval);
                    }
                }, 50);
            } catch (error) {
                console.log('Reprodução automática bloqueada pelo navegador');
            }
        }
    }
    
    async playClickSound() {
        if (!this.isMuted) {
            // Adicionar à fila de cliques
            this.clickQueue.push(Date.now());
        }
    }
    
    processClickQueue() {
        if (this.clickQueue.length > 0 && !this.isMuted) {
            // Reproduzir o som mais antigo da fila
            const clickSound = this.clickSound.cloneNode();
            clickSound.volume = 0.5;
            clickSound.play().catch(error => {
                console.log('Erro ao reproduzir som de clique');
            });
            
            // Limpar a fila
            this.clickQueue = [];
        }
    }
    
    async muteAll() {
        // Fade out antes de pausar
        if (this.musicPlaying) {
            const fadeInterval = setInterval(() => {
                if (this.backgroundMusic.volume > 0) {
                    this.backgroundMusic.volume -= 0.01;
                } else {
                    clearInterval(fadeInterval);
                    this.backgroundMusic.pause();
                }
            }, 50);
        }
        
        this.isMuted = true;
        this.musicPlaying = false;
        localStorage.setItem('audioMuted', 'true');
    }
    
    async unmuteAll() {
        this.isMuted = false;
        localStorage.setItem('audioMuted', 'false');
        await this.playBackgroundMusic();
    }
    
    async toggleMute() {
        if (this.isMuted) {
            await this.unmuteAll();
        } else {
            await this.muteAll();
        }
    }
}

// Inicializar o gerenciador de áudio quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.audioManager = new AudioManager();
    
    // Adicionar botão de controle de áudio com animação
    const audioControl = document.createElement('button');
    audioControl.id = 'audioControl';
    audioControl.className = 'audio-control';
    audioControl.innerHTML = '<i class="fas fa-volume-up"></i>';
    document.body.appendChild(audioControl);
    
    // Adicionar evento de clique para todos os botões com feedback visual
    document.querySelectorAll('button, .btn').forEach(button => {
        button.addEventListener('click', async () => {
            // Adicionar classe de animação
            button.classList.add('button-clicked');
            
            // Reproduzir som com delay
            await window.audioManager.playClickSound();
            
            // Remover classe após a animação
            setTimeout(() => {
                button.classList.remove('button-clicked');
            }, 200);
        });
    });
    
    // Evento para toggle do áudio com animação
    audioControl.addEventListener('click', async () => {
        audioControl.classList.add('button-clicked');
        await window.audioManager.toggleMute();
        
        const icon = audioControl.querySelector('i');
        icon.className = window.audioManager.isMuted ? 'fas fa-volume-mute' : 'fas fa-volume-up';
        
        setTimeout(() => {
            audioControl.classList.remove('button-clicked');
        }, 200);
    });
    
    // Iniciar música de fundo quando houver interação do usuário
    document.addEventListener('click', () => {
        window.audioManager.playBackgroundMusic();
    }, { once: true });
}); 
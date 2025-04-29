class AudioManager {
    constructor() {
        if (window.audioManager) {
            return window.audioManager; // Singleton pattern
        }

        // Inicializar variáveis de áudio
        this.backgroundMusic = new Audio('/static/audio/background.mp3');
        this.clickSound = new Audio('/static/audio/click.mp3');
        
        // Configurar música de fundo
        this.backgroundMusic.loop = true;
        this.backgroundMusic.volume = 0;  // Começar com volume 0 para fade in
        
        // Configurar som de clique
        this.clickSound.volume = 0.5;
        
        // Estado do áudio
        this.isMuted = false;
        this.musicPlaying = false;
        this.isClickReady = true;
        this.clickQueue = [];
        this.fadeInterval = null;
        this.currentTime = 0;
        
        // Carregar preferências do usuário
        this.loadPreferences();
        
        // Configurar intervalo para processar a fila de cliques
        setInterval(() => this.processClickQueue(), 2000);

        // Salvar estado da música antes de navegar
        window.addEventListener('beforeunload', () => {
            if (this.musicPlaying && !this.isMuted) {
                localStorage.setItem('musicPlaying', 'true');
                localStorage.setItem('musicTime', this.backgroundMusic.currentTime);
            } else {
                localStorage.setItem('musicPlaying', 'false');
            }
        });

        // Guardar instância
        window.audioManager = this;
    }
    
    loadPreferences() {
        const muted = localStorage.getItem('audioMuted') === 'true';
        const wasPlaying = localStorage.getItem('musicPlaying') === 'true';
        const savedTime = parseFloat(localStorage.getItem('musicTime')) || 0;
        
        this.isMuted = muted;
        
        if (wasPlaying && !muted) {
            this.backgroundMusic.currentTime = savedTime;
            // Atrasar o início da música para evitar problemas de carregamento
            setTimeout(() => {
                this.playBackgroundMusic(true);
            }, 1000);
        }
    }
    
    async playBackgroundMusic(resume = false) {
        if ((!this.musicPlaying && !this.isMuted) || resume) {
            try {
                // Limpar qualquer fade interval existente
                if (this.fadeInterval) {
                    clearInterval(this.fadeInterval);
                }

                // Resetar o volume apenas se não estiver resumindo
                if (!resume) {
                    this.backgroundMusic.volume = 0;
                }

                // Delay inicial apenas se não estiver resumindo
                if (!resume) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
                
                // Verificar novamente se não está mutado antes de tocar
                if (!this.isMuted) {
                    await this.backgroundMusic.play();
                    this.musicPlaying = true;
                    
                    // Configurar fade in
                    let volume = this.backgroundMusic.volume;
                    this.fadeInterval = setInterval(() => {
                        if (volume < 0.3 && !this.isMuted) {
                            volume += 0.01;
                            this.backgroundMusic.volume = volume;
                        } else {
                            clearInterval(this.fadeInterval);
                            this.fadeInterval = null;
                        }
                    }, 50);
                }
            } catch (error) {
                console.log('Reprodução automática bloqueada pelo navegador');
                this.musicPlaying = false;
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
        // Limpar qualquer fade interval existente
        if (this.fadeInterval) {
            clearInterval(this.fadeInterval);
            this.fadeInterval = null;
        }

        // Fade out antes de pausar
        if (this.musicPlaying) {
            const startVolume = this.backgroundMusic.volume;
            this.fadeInterval = setInterval(() => {
                if (this.backgroundMusic.volume > 0) {
                    this.backgroundMusic.volume = Math.max(0, this.backgroundMusic.volume - 0.01);
                } else {
                    clearInterval(this.fadeInterval);
                    this.fadeInterval = null;
                    this.backgroundMusic.pause();
                }
            }, 50);
        }
        
        this.isMuted = true;
        this.musicPlaying = false;
        localStorage.setItem('audioMuted', 'true');
        localStorage.setItem('musicPlaying', 'false');
    }
    
    async unmuteAll() {
        this.isMuted = false;
        localStorage.setItem('audioMuted', 'false');
        
        // Se a música já estiver tocando, apenas restaurar o volume
        if (this.backgroundMusic.paused) {
            await this.playBackgroundMusic(true);
        } else {
            // Fade in
            if (this.fadeInterval) {
                clearInterval(this.fadeInterval);
            }
            
            let volume = this.backgroundMusic.volume;
            this.fadeInterval = setInterval(() => {
                if (volume < 0.3) {
                    volume += 0.01;
                    this.backgroundMusic.volume = volume;
                } else {
                    clearInterval(this.fadeInterval);
                    this.fadeInterval = null;
                }
            }, 50);
        }
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
    // Verificar se já existe uma instância
    if (!window.audioManager) {
        window.audioManager = new AudioManager();
    }
    
    // Adicionar botão de controle de áudio com animação
    if (!document.getElementById('audioControl')) {
        const audioControl = document.createElement('button');
        audioControl.id = 'audioControl';
        audioControl.className = 'audio-control';
        audioControl.innerHTML = '<i class="fas fa-volume-up"></i>';
        document.body.appendChild(audioControl);
        
        // Atualizar o ícone inicial baseado no estado
        const icon = audioControl.querySelector('i');
        icon.className = window.audioManager.isMuted ? 'fas fa-volume-mute' : 'fas fa-volume-up';
        
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
    }
    
    // Adicionar evento de clique para todos os botões com feedback visual
    document.querySelectorAll('button, .btn').forEach(button => {
        if (!button.hasClickHandler) {
            button.hasClickHandler = true;
            button.addEventListener('click', async () => {
                button.classList.add('button-clicked');
                await window.audioManager.playClickSound();
                setTimeout(() => {
                    button.classList.remove('button-clicked');
                }, 200);
            });
        }
    });
    
    // Iniciar música de fundo quando houver interação do usuário
    if (!document.hasBackgroundMusicHandler) {
        document.hasBackgroundMusicHandler = true;
        document.addEventListener('click', () => {
            window.audioManager.playBackgroundMusic();
        }, { once: true });
    }
}); 
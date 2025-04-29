"""
Arquivo de configuração de exemplo.
Renomeie para config.py e ajuste as configurações conforme necessário.
NÃO comite o arquivo config.py real com suas chaves!
"""

# Configurações do Flask
DEBUG = False  # Mude para True em desenvolvimento
SECRET_KEY = 'sua-chave-secreta-aqui'  # ⚠️ Mude isto em produção!

# Configurações de Segurança
CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'outra-chave-secreta-aqui'  # ⚠️ Mude isto em produção!

# Configurações do Servidor
HOST = '0.0.0.0'
PORT = 5000

# Rate Limiting
RATELIMIT_DEFAULT = "200 per day"
RATELIMIT_STORAGE_URL = "memory://"

# Configurações SSL/TLS (para produção)
SSL_CERT_PATH = None  # Caminho para certificado SSL
SSL_KEY_PATH = None   # Caminho para chave privada SSL

# Configurações de Cache
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300

# Configurações de Segurança Adicional
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True

# Headers de Segurança
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
}

class Config:
    # Configurações Básicas
    DEBUG = False
    TESTING = False
    PORT = 5000
    HOST = '0.0.0.0'
    
    # Chaves de Segurança (substitua por valores seguros)
    SECRET_KEY = 'substitua-por-uma-chave-secreta-segura'
    WTF_CSRF_SECRET_KEY = 'substitua-por-uma-chave-csrf-segura'
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "100/day"
    RATELIMIT_STORAGE_URL = "memory://"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Configurações específicas de produção
    DEBUG = False
    
    # Recomendado usar variáveis de ambiente em produção
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') 
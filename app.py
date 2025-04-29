from flask import Flask, request, render_template, session, redirect, url_for, jsonify, send_from_directory, flash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import secrets
import logging
from logging.handlers import RotatingFileHandler
import math
import sqlite3
from flask_wtf.csrf import generate_csrf
import re

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging com formato mais detalhado
if not os.path.exists('logs'):
    os.makedirs('logs')

formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] - %(message)s\n'
    'File: %(pathname)s\n'
    'Function: %(funcName)s\n'
    'Line: %(lineno)d\n'
    'Details: %(message)s\n'
)

# Configurar logger da aplicação
logger = logging.getLogger('imc_calculator')
logger.setLevel(logging.DEBUG)

# Configurar console handler em vez de file handler para desenvolvimento
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# Inicializar Sentry para monitoramento de erros em produção
if os.getenv('SENTRY_DSN'):
    logger.info('Inicializando Sentry para monitoramento de erros')
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv('FLASK_ENV', 'production')
    )

app = Flask(__name__)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

logger.info('Iniciando aplicação Flask')

# Configurações de segurança
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hora

logger.info('Configurações de segurança aplicadas')

# Inicializar extensões de segurança
csrf = CSRFProtect()
csrf.init_app(app)
logger.info('Proteção CSRF inicializada')

# Tratamento de erro CSRF
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.warning(f'Erro CSRF detectado: {str(e)}')
    return render_template('index.html', erro="Erro de segurança: Por favor, tente novamente."), 400

# Configurar Talisman com base no ambiente
is_production = os.getenv('FLASK_ENV') == 'production'
Talisman(app, 
    force_https=is_production,
    strict_transport_security=is_production,
    session_cookie_secure=is_production,
    content_security_policy={
        'default-src': "'self'",
        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
        'script-src': ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
        'font-src': ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
        'img-src': ["'self'", "data:", "https:"],
        'connect-src': ["'self'"],
        'frame-ancestors': ["'none'"],
        'form-action': ["'self'"],
        'base-uri': ["'self'"],
        'frame-src': ["'none'"]
    } if is_production else None
)
logger.info(f'Talisman configurado para ambiente: {"produção" if is_production else "desenvolvimento"}')

# Configurar limitação de taxa de requisições
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
logger.info('Rate limiting configurado')

# Configurar caminho do banco de dados
if os.getenv('FLASK_ENV') == 'production':
    DB_PATH = '/data/imc_calculator.db'
else:
    DB_PATH = 'imc_calculator.db'

def init_db():
    logger.info('Iniciando configuração do banco de dados')
    try:
        # Criar diretório de dados se não existir em produção
        if os.getenv('FLASK_ENV') == 'production':
            os.makedirs('/data', exist_ok=True)
            
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Criar tabela com índices otimizados
        c.execute('''CREATE TABLE IF NOT EXISTS historico_imc
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT NOT NULL,
                      idade INTEGER NOT NULL CHECK (idade > 0 AND idade <= 120),
                      sexo TEXT NOT NULL CHECK (sexo IN ('masculino', 'feminino')),
                      peso REAL NOT NULL CHECK (peso > 0 AND peso <= 300),
                      altura REAL NOT NULL CHECK (altura > 0 AND altura <= 3),
                      imc REAL NOT NULL,
                      nivel_atividade TEXT NOT NULL CHECK (nivel_atividade IN 
                        ('sedentario', 'leve', 'moderado', 'intenso', 'muito_intenso')),
                      data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Criar índices para otimização de consultas
        c.execute('''CREATE INDEX IF NOT EXISTS idx_historico_imc_nome 
                     ON historico_imc(nome)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_historico_imc_data 
                     ON historico_imc(data)''')
        
        conn.commit()
        conn.close()
        logger.info('Banco de dados configurado com sucesso')
    except Exception as e:
        logger.error(f'Erro ao configurar banco de dados: {str(e)}')
        raise

init_db()

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do Peso"
    elif imc < 24.9:
        return "Peso Normal"
    elif imc < 29.9:
        return "Sobrepeso"
    elif imc < 34.9:
        return "Obesidade Grau I"
    elif imc < 39.9:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def calcular_peso_ideal(altura, sexo):
    if sexo.lower() == 'masculino':
        peso_ideal = (72.7 * altura) - 58
        margem = 2.5
    else:
        peso_ideal = (62.1 * altura) - 44.7
        margem = 2.0
    
    return (peso_ideal - margem, peso_ideal + margem)

def calcular_massa_magra(peso, altura, idade, sexo):
    if sexo.lower() == 'masculino':
        massa_magra = peso * (1 - (0.20 + (idade - 20) * 0.001))  # 20% base + 0.1% por ano acima de 20
    else:
        massa_magra = peso * (1 - (0.25 + (idade - 20) * 0.001))  # 25% base + 0.1% por ano acima de 20
    return max(round(massa_magra, 1), peso * 0.5)  # Garantir que não seja menor que 50% do peso

def calcular_gordura_corporal(peso, massa_magra):
    gordura = ((peso - massa_magra) / peso) * 100
    return round(gordura, 1)

def classificar_gordura_corporal(gordura, sexo):
    if sexo.lower() == 'masculino':
        if gordura < 6:
            return "Gordura essencial"
        elif gordura < 14:
            return "Atleta"
        elif gordura < 18:
            return "Fitness"
        elif gordura < 25:
            return "Aceitável"
        else:
            return "Obesidade"
    else:
        if gordura < 12:
            return "Gordura essencial"
        elif gordura < 20:
            return "Atleta"
        elif gordura < 24:
            return "Fitness"
        elif gordura < 31:
            return "Aceitável"
        else:
            return "Obesidade"

def calcular_gasto_calorico(peso, altura, idade, sexo, nivel_atividade):
    # Cálculo do Metabolismo Basal (TMB)
    if sexo.lower() == 'masculino':
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura * 100) - (5.677 * idade)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura * 100) - (4.330 * idade)

    # Fator de atividade
    fatores = {
        'sedentario': 1.2,
        'leve': 1.375,
        'moderado': 1.55,
        'intenso': 1.725,
        'muito_intenso': 1.9
    }
    
    fator = fatores.get(nivel_atividade.lower(), 1.2)
    gasto_total = tmb * fator
    
    return round(tmb), round(gasto_total)

def calcular_agua_diaria(peso, nivel_atividade):
    base = peso * 35  # 35ml por kg de peso
    
    fatores = {
        'sedentario': 1.0,
        'leve': 1.1,
        'moderado': 1.2,
        'intenso': 1.3,
        'muito_intenso': 1.4
    }
    
    fator = fatores.get(nivel_atividade.lower(), 1.0)
    return round((base * fator) / 1000, 1)  # Convertendo para litros

def gerar_plano_nutricional(categoria_imc, gordura_corporal):
    plano = "<ul>"
    
    # Recomendações base
    plano += "<li>Mantenha uma dieta balanceada com proteínas magras, carboidratos complexos e gorduras boas</li>"
    plano += "<li>Faça 5-6 refeições menores ao longo do dia</li>"
    
    if categoria_imc == "Abaixo do Peso":
        plano += "<li>Aumente a ingestão calórica de forma saudável</li>"
        plano += "<li>Priorize alimentos calóricos nutritivos como abacate, nuts e azeite</li>"
    elif "Obesidade" in categoria_imc:
        plano += "<li>Crie um déficit calórico moderado e sustentável</li>"
        plano += "<li>Evite alimentos processados e açúcares refinados</li>"
    
    if gordura_corporal > 25:
        plano += "<li>Aumente o consumo de proteínas magras</li>"
        plano += "<li>Reduza o consumo de carboidratos simples</li>"
    
    plano += "</ul>"
    return plano

def gerar_plano_exercicios(categoria_imc, nivel_atividade):
    plano = "<ul>"
    
    if nivel_atividade.lower() == 'sedentario':
        plano += "<li>Comece com caminhadas leves de 15-20 minutos, 3x por semana</li>"
        plano += "<li>Gradualmente aumente para 30 minutos, 5x por semana</li>"
    
    if "Obesidade" in categoria_imc:
        plano += "<li>Foque em exercícios de baixo impacto como natação ou bicicleta</li>"
        plano += "<li>Inclua exercícios de força 2-3x por semana</li>"
    else:
        plano += "<li>Combine exercícios aeróbicos e de força</li>"
        plano += "<li>Tente acumular 150 minutos de atividade moderada por semana</li>"
    
    if nivel_atividade.lower() in ['intenso', 'muito_intenso']:
        plano += "<li>Mantenha um programa variado de exercícios</li>"
        plano += "<li>Inclua períodos adequados de recuperação</li>"
        plano += "<li>Considere trabalhar com um profissional para otimizar seu treino</li>"
    
    plano += "</ul>"
    return plano

@app.template_filter('now')
def now_filter(format_string):
    return datetime.now().strftime(format_string)

# Proteção contra XSS nos campos de entrada
def sanitize_input(text):
    if not text:
        return text
    # Remove tags HTML maliciosos
    text = re.sub(r'<[^>]*?>', '', text)
    # Escapa caracteres especiais
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    return text

@app.before_request
def before_request():
    if not request.is_secure and is_production:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

@app.route("/", methods=['GET'])
@limiter.limit("5 per minute")
def home():
    try:
        logger.info('Acessando página inicial')
        return render_template('index.html')
    except Exception as e:
        logger.error(f'Erro ao renderizar página inicial: {str(e)}')
        return render_template('error.html', error="Erro interno do servidor"), 500

@app.route("/calcular", methods=["POST"])
@limiter.limit("5 per minute")
def calcular():
    try:
        logger.info('=== Início do processamento do formulário ===')
        logger.info(f'Headers: {dict(request.headers)}')
        logger.info(f'Form data: {dict(request.form)}')
        
        # Verificar CSRF token
        if not request.form.get('csrf_token'):
            logger.error('CSRF token ausente')
            return render_template('index.html', erro="Erro de segurança: token ausente")

        # Obter e validar dados do formulário
        dados = {}
        try:
            dados['nome'] = sanitize_input(request.form.get('nome', '').strip())
            if not dados['nome'] or len(dados['nome']) < 2:
                raise ValueError("Nome inválido")

            dados['idade'] = int(sanitize_input(request.form.get('idade', '0')))
            if dados['idade'] < 1 or dados['idade'] > 120:
                raise ValueError("Idade deve estar entre 1 e 120 anos")

            dados['sexo'] = sanitize_input(request.form.get('sexo', '').lower())
            if dados['sexo'] not in ['masculino', 'feminino']:
                raise ValueError("Sexo inválido")

            dados['peso'] = float(sanitize_input(request.form.get('peso', '0').replace(',', '.')))
            if dados['peso'] < 1 or dados['peso'] > 300:
                raise ValueError("Peso deve estar entre 1 e 300 kg")

            dados['altura'] = float(sanitize_input(request.form.get('altura', '0').replace(',', '.')))
            if dados['altura'] < 0.5 or dados['altura'] > 3:
                raise ValueError("Altura deve estar entre 0.5 e 3 metros")

            dados['nivel_atividade'] = sanitize_input(request.form.get('nivel_atividade', '').lower())
            if dados['nivel_atividade'] not in ['sedentario', 'leve', 'moderado', 'intenso', 'muito_intenso']:
                raise ValueError("Nível de atividade inválido")

            logger.info(f'Dados validados com sucesso: {dados}')

        except ValueError as e:
            logger.error(f'Erro na validação dos dados: {str(e)}')
            return render_template('index.html', erro=str(e))

        # Realizar cálculos
        try:
            resultados = {}
            resultados.update(dados)

            # IMC
            resultados['imc'] = calcular_imc(dados['peso'], dados['altura'])
            logger.info(f'IMC calculado: {resultados["imc"]}')
            
            resultados['categoria'] = classificar_imc(resultados['imc'])
            logger.info(f'Categoria IMC: {resultados["categoria"]}')
            
            # Peso ideal
            resultados['peso_ideal_min'], resultados['peso_ideal_max'] = calcular_peso_ideal(dados['altura'], dados['sexo'])
            logger.info(f'Peso ideal: {resultados["peso_ideal_min"]} - {resultados["peso_ideal_max"]}')
            
            # Massa magra e gordura
            resultados['massa_magra'] = calcular_massa_magra(dados['peso'], dados['altura'], dados['idade'], dados['sexo'])
            logger.info(f'Massa magra: {resultados["massa_magra"]}')
            
            resultados['gordura_corporal'] = calcular_gordura_corporal(dados['peso'], resultados['massa_magra'])
            logger.info(f'Gordura corporal: {resultados["gordura_corporal"]}')
            
            resultados['classificacao_gordura'] = classificar_gordura_corporal(resultados['gordura_corporal'], dados['sexo'])
            logger.info(f'Classificação gordura: {resultados["classificacao_gordura"]}')
            
            # Gasto calórico
            resultados['tmb'], resultados['gasto_calorico'] = calcular_gasto_calorico(
                dados['peso'], dados['altura'], dados['idade'], dados['sexo'], dados['nivel_atividade']
            )
            logger.info(f'TMB: {resultados["tmb"]}, Gasto calórico: {resultados["gasto_calorico"]}')
            
            # Água
            resultados['agua_diaria'] = calcular_agua_diaria(dados['peso'], dados['nivel_atividade'])
            logger.info(f'Água diária: {resultados["agua_diaria"]}')

            # Recomendações
            resultados['plano_nutricional'] = gerar_plano_nutricional(resultados['categoria'], resultados['gordura_corporal'])
            resultados['plano_exercicios'] = gerar_plano_exercicios(resultados['categoria'], dados['nivel_atividade'])

            logger.info('=== Cálculos realizados com sucesso ===')
            logger.info(f'Resultados finais: {resultados}')

            # Data atual formatada
            resultados['data_atual'] = datetime.now().strftime('%d/%m/%Y às %H:%M')

            return render_template('resultado.html', **resultados)

        except Exception as calc_error:
            logger.error(f'Erro nos cálculos: {str(calc_error)}', exc_info=True)
            return render_template('index.html', erro="Erro ao realizar os cálculos. Por favor, verifique os valores inseridos.")

    except Exception as e:
        logger.error(f'Erro não tratado: {str(e)}', exc_info=True)
        return render_template('index.html', erro="Erro ao processar os dados. Por favor, tente novamente.")

@app.route("/analise")
@limiter.limit("20 per minute")  # 20 requisições por minuto
def analise():
    logger.info('Acessando página de análise')
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''SELECT nome, peso, altura, imc, data 
                     FROM historico_imc 
                     ORDER BY data DESC 
                     LIMIT 10''')
        historico = c.fetchall()
        conn.close()
        
        logger.debug(f'Registros recuperados: {len(historico)}')
        return render_template(
            "analise.html",
            historico=historico
        )
    except Exception as e:
        logger.error(f'Erro na análise: {str(e)}', exc_info=True)
        return render_template("500.html"), 500

@app.route("/privacidade")
def privacidade():
    logger.info('Acessando página de privacidade')
    try:
        return render_template("privacidade.html")
    except Exception as e:
        logger.error(f'Erro na página de privacidade: {str(e)}', exc_info=True)
        return render_template("500.html"), 500

@app.route("/termos")
def termos():
    logger.info('Acessando página de termos')
    try:
        return render_template("termos.html")
    except Exception as e:
        logger.error(f'Erro na página de termos: {str(e)}', exc_info=True)
        return render_template("500.html"), 500

@app.route("/get_csrf_token")
def get_csrf_token():
    return jsonify({"csrf_token": generate_csrf()})

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f'Rate limit excedido: {str(e)}')
    return render_template("index.html", erro="Muitas requisições. Por favor, aguarde um momento."), 429

@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f'Página não encontrada: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Erro interno do servidor: {str(error)}', exc_info=True)
    return render_template('500.html'), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/historico")
@limiter.limit("20 per minute")
def historico():
    logger.info('Acessando página de histórico')
    try:
        return render_template("historico.html")
    except Exception as e:
        logger.error(f'Erro na página de histórico: {str(e)}', exc_info=True)
        return render_template("500.html"), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f'Iniciando servidor na porta {port}')
    app.run(host="0.0.0.0", port=port)
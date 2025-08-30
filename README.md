# 🔥 FURIOUSOFNIGHT SUPER PERFORMANCE

<div align="center">

![Logo FURIOUSOFNIGHT](static/img/logo.png)

🎯LINK PARA TESTE https://project-imc.fly.dev/ 🎯

Uma calculadora de IMC de última geração com análise corporal avançada e interface cyberpunk.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)
[![TikTok](https://img.shields.io/badge/TikTok-Follow-black?style=for-the-badge&logo=tiktok)](https://www.tiktok.com/@furiousofnightgames)

[Funcionalidades](#-funcionalidades) • 
[Demonstração](#-demonstração) • 
[Instalação](#%EF%B8%8F-instalação) • 
[Tecnologias](#-tecnologias) • 
[Arquitetura](#-arquitetura) • 
[Segurança](#-segurança) • 
[Contribuindo](#-contribuindo)

</div>

## 📋 Sobre o Projeto

O FURIOUSOFNIGHT SUPER PERFORMANCE é uma aplicação web moderna para análise corporal completa, oferecendo muito mais que um simples cálculo de IMC. Com uma interface cyberpunk impressionante e recursos avançados de análise, a aplicação fornece recomendações personalizadas baseadas em dados científicos.

### ✨ Funcionalidades

#### Análise Corporal Avançada
- 📊 Cálculo preciso de IMC com classificação detalhada
- 🎯 Análise de composição corporal (massa magra e gordura)
- 💪 Cálculo de massa muscular estimada
- 🔥 Estimativa de gasto calórico basal e total

#### Recomendações Personalizadas
- 🥗 Planos nutricionais básicos adaptados ao perfil
- 💪 Sugestões de exercícios baseados na condição física
- 💧 Cálculo de hidratação diária recomendada
- ⚡ Dicas de suplementação básica

#### Interface Moderna
- 🎨 Design cyberpunk/neon imersivo
- 🔊 Sistema de áudio interativo para feedback
- 📱 Layout totalmente responsivo
- 🌙 Modo escuro automático

## 🎮 Demonstração

<div align="center">

![Demo da Aplicação](static/img/demo.gif)

[Acesse a Demo Online](https://super-performance.fly.dev)

</div>

## 🛠️ Tecnologias

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask** - Framework web
- **SQLite** - Banco de dados
- **Flask-WTF** - Segurança de formulários
- **Flask-Limiter** - Controle de taxa de requisições
- **Flask-Talisman** - Segurança HTTPS

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript (ES6+)** - Interatividade
- **Web Audio API** - Sistema de áudio
- **LocalStorage API** - Armazenamento local

### Segurança
- **CSRF Protection** - Proteção contra ataques CSRF
- **Rate Limiting** - Prevenção de abusos
- **Input Sanitization** - Proteção contra XSS
- **Content Security Policy** - Segurança de conteúdo
- **HTTPS Enforcement** - Criptografia de dados

## ⚙️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/furiousofnight-super-performance.git
cd furiousofnight-super-performance
```

2. Configure o ambiente virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados
```bash
flask db upgrade
```

6. Execute a aplicação
```bash
flask run
```

## 📐 Arquitetura

```
furiousofnight-super-performance/
├── app/
│   ├── models/         # Modelos de dados
│   ├── controllers/    # Controladores
│   ├── services/       # Lógica de negócios
│   └── utils/         # Utilitários
├── static/
│   ├── css/           # Estilos
│   ├── js/            # Scripts
│   ├── audio/         # Arquivos de áudio
│   └── img/           # Imagens
├── templates/         # Templates HTML
├── tests/            # Testes unitários
└── docs/             # Documentação
```

## 🔒 Segurança

### Proteções Implementadas
- ✅ Sanitização de inputs
- ✅ Proteção CSRF
- ✅ Rate limiting
- ✅ Headers de segurança
- ✅ HTTPS forçado
- ✅ CSP configurado

### Boas Práticas
- 🔐 Sem armazenamento de dados sensíveis
- 🔒 Sessões seguras
- 🛡️ Validação de dados
- 📝 Logs de segurança

## 🚀 Deploy

### Requisitos de Produção
1. Servidor com Python 3.8+
2. Servidor WSGI (Gunicorn recomendado)
3. Proxy reverso (Nginx recomendado)
4. Certificado SSL/TLS

### Configuração de Produção
```bash
# Variáveis de ambiente necessárias
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///production.db
```

## 📈 Performance

- ⚡ Tempo de resposta médio: <100ms
- 🔄 Cache implementado
- 📦 Assets minificados
- 🖼️ Imagens otimizadas

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit suas mudanças
```bash
git commit -m 'Add: nova funcionalidade incrível'
```
4. Push para a Branch
```bash
git push origin feature/AmazingFeature
```
5. Abra um Pull Request

### Guia de Contribuição
- 📝 Siga o padrão de commits
- ✅ Adicione testes para novas funcionalidades
- 📚 Atualize a documentação
- 🎨 Siga o guia de estilo de código

## 👤 Autor

**FURIOUSOFNIGHT**

- 🎮 TikTok: [@furiousofnightgames](https://www.tiktok.com/@furiousofnightgames)
- 💻 GitHub: [@furiousofnight](https://github.com/furiousofnight)

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

Feito com 🖤 por [FURIOUSOFNIGHT](https://www.tiktok.com/@furiousofnightgames)

</div>

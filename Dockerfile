# Usando Python 3.13.3
FROM python:3.13.3-slim

# Instalar dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-server-dev-all \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -r appuser

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Criar diretório de logs com permissões corretas
RUN mkdir -p logs && chown -R appuser:appuser logs

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Mudar para usuário não-root
USER appuser

# Expor a porta (Fly.io usa a porta 8080 como padrão)
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
# Usando uma imagem base leve do Python 3.13.3
FROM python:3.13.3-slim

# Criar diretório na imagem para a aplicação
WORKDIR /app

# Copiar os seus arquivos para o contêiner
COPY . /app

# Instalar dependências do aplicativo usando o arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta (Fly.io usa a porta 8080 como padrão)
EXPOSE 8080

# Comando para iniciar o servidor com Gunicorn para produção
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
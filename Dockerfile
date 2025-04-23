# Usando uma imagem base leve do Python
FROM python:3.9-slim

# Criar diretório na imagem para a aplicação
WORKDIR /app

# Copiar os seus arquivos para o contêiner
COPY . /app

# Instalar dependências do aplicativo usando o arquivo requirements.txt
RUN pip install -r requirements.txt

# Expor a porta (Fly.io usa a porta 8080 como padrão)
EXPOSE 8080

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]
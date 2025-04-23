# 📝 Calculadora de IMC com Flask

Este é um aplicativo simples e interativo para calcular o Índice de Massa Corporal (**IMC**) de usuários, desenvolvido com a biblioteca Flask. Ele permite que o usuário insira seu peso e altura e, com base nesses dados, exibe o valor do IMC, a categoria correspondente e recomendações personalizadas (alimentação, exercícios e cuidados médicos).

O propósito deste projeto é servir como um exemplo prático para aprender Flask ou ser potencialmente expandido para aplicações maiores.

---

## 📋 Funcionalidades

- Exibe um formulário para inserção de **nome**, **peso** e **altura**.
- Calcula o Índice de Massa Corporal (IMC) do usuário.
- Classifica o resultado do IMC em diferentes categorias:
  - Abaixo do peso
  - Peso ideal
  - Sobrepeso
  - Obesidade Grau I, II ou Mórbida.
- Exibe recomendações detalhadas de:
  - Alimentação.
  - Atividades físicas adequadas.
  - Cuidados médicos sugeridos.
- Armazena o histórico de cálculos do usuário na sessão do navegador.
- Validação de entradas garantindo que sejam dentro de intervalos plausíveis para peso e altura.

---

## 🎯 Índice de Massa Corporal

O **IMC** é calculado utilizando a fórmula:

```
IMC = peso (kg) / altura² (m²)
```


As categorias e faixas disponíveis no aplicativo são:
| **Faixa de IMC** | **Classificação**           |
|-------------------|-----------------------------|
| Menor que 18.5    | Abaixo do Peso             |
| Entre 18.5 e 24.9 | Peso Ideal                 |
| Entre 25 e 29.9   | Sobrepeso                  |
| Entre 30 e 34.9   | Obesidade Grau I           |
| Entre 35 e 39.9   | Obesidade Grau II          |
| Maior que 40      | Obesidade Mórbida          |

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)**: Linguagem principal para o backend.
- **[Flask](https://flask.palletsprojects.com/)**: Microframework web utilizado para construir e renderizar o aplicativo.
- **HTML5** + **CSS3**: Responsáveis pela interface gráfica.
- **Bootstrap (opcional)**: Pode ser integrado no futuro para melhorar a responsividade (atualmente não utilizado).
- **JavaScript (opcional)**: Extensões simples ou futuras melhorias.

---

## 📁 Estrutura do Projeto

Um guia rápido para os arquivos e diretórios do projeto:

```
/meu_app_imc              # Diretório raiz do projeto
├── /templates            # Diretório para templates HTML
│   ├── index.html        # Página inicial do app (formulário de entrada)
│   └── resultado.html    # Página de resultado do cálculo de IMC
├── /static               # Diretório para arquivos estáticos
│   ├── /css
│   │   └── styles.css    # Estilização do app
│   ├── /js
│   │   └── scripts.js    # Scripts futuros (opcional)
│   └── /img              # Imagens do app (opcional)
├── app.py                # Arquivo principal do aplicativo Flask
├── requirements.txt      # Lista de dependências do projeto
└── README.md             # Documentação completa do projeto
```


---

## 🚀 Guia de Instalação

Siga os passos abaixo para rodar o projeto localmente.

### Pré-requisitos

- Python 3.7+ instalado ([download aqui](https://www.python.org/downloads/)).
- Ferramenta Git ou client GitHub para clonar o repositório (opcional).

---

### Clonar o Repositório

Se você ainda não baixou o projeto, clone-o a partir do GitHub:

```shell script
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```


---

### Configurar o Ambiente Virtual (Recomendado)

1. Crie um ambiente virtual:
```shell script
python -m venv venv
```


2. Ative o ambiente virtual:
   - **Linux/Mac**:
```shell script
source venv/bin/activate
```

   - **Windows**:
```shell script
venv\Scripts\activate
```


---

### Instalar as Dependências

Instale os pacotes necessários para rodar o aplicativo:

```shell script
pip install -r requirements.txt
```


---

### Executar o Projeto

Inicie o servidor Flask:

```shell script
python app.py
```


O aplicativo estará disponível no navegador na URL:

```
http://127.0.0.1:5000
```


---

### Dependências (requirements.txt)

Atualmente, o projeto depende do Flask. Certifique-se de que ele está listado no arquivo **`requirements.txt`**:

```
Flask==2.3.2
```


---

## 🧩 Como Usar

1. Acesse a página inicial: `http://127.0.0.1:5000`.
2. Preencha o formulário com seu **nome**, **peso** (em kg) e **altura** (em metros).
3. Clique no botão "Calcular IMC".
4. Veja o resultado do cálculo, incluindo:
   - Mensagem saudando o usuário com o valor do IMC calculado.
   - Categoria do IMC.
   - Recomendações personalizadas para saúde, alimentação e cuidados médicos.
5. O aplicativo mostrará, na página inicial, um **histórico de cálculos** da sessão atual.

---

## 📚 Exemplos de Uso

### Exemplo 1 - João:
- Nome: João
- Peso: **72 kg**
- Altura: **1.75 m**

**Resultado**:
- IMC: 23.5
- Categoria: Peso Ideal
- Recomendações: Continue com alimentação balanceada e práticas regulares de exercícios leves.

### Exemplo 2 - Maria:
- Nome: Maria
- Peso: **95 kg**
- Altura: **1.65 m**

**Resultado**:
- IMC: 34.9
- Categoria: Obesidade Grau I
- Recomendações: Consulte um endocrinologista para estratégias de perda de peso e priorize vegetais e atividades de baixo impacto.

---

## 👥 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

- Faça um fork do repositório.
- Crie uma branch para suas alterações:
```shell script
git checkout -b feature/nova-funcionalidade
```

- Faça commit das alterações:
```shell script
git commit -m 'Adicionei uma nova funcionalidade'
```

- Suba as alterações para sua branch:
```shell script
git push origin feature/nova-funcionalidade
```

- Abra um **pull request** explicando as mudanças realizadas.

---

## 🛡️ Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo **LICENSE** para detalhes.

---

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma [Issue](https://github.com/seu-usuario/nome-do-repositorio/issues) no GitHub.

---

Agora você pode copiar o README acima e colá-lo diretamente no seu arquivo **`README.md`** do repositório no GitHub!😊
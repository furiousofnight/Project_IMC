from flask import Flask, request, render_template, session
from datetime import datetime
import os  # Para acessar variáveis de ambiente futuramente

app = Flask(__name__)

# Configuração da Secret Key
# Em um ambiente como Fly.io, você usará a variável de ambiente FLASK_SECRET_KEY
app.secret_key = os.getenv("FLASK_SECRET_KEY", "uma-chave-segura-e-padrao")  # Substituir em produção!

# Validação rigorosa de dados enviados pelo usuário
def validar_dados(peso, altura):
    if altura <= 0 or altura > 2.5:  # Limite: 2.5m (altura humana plausível)
        raise ValueError("Altura inválida. Deve estar entre 0.5m e 2.5m.")
    if peso <= 0 or peso > 300:  # Peso humano até 300kg
        raise ValueError("Peso inválido. Deve estar entre 2kg e 300kg.")

@app.route("/")
def home():
    historico = session.get("historico", [])
    return render_template("index.html", historico=historico)

@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        # Capturando as entradas do formulário
        nome = request.form.get("nome", "Visitante").strip().capitalize()
        peso_str = request.form.get("peso", "").strip()
        altura_str = request.form.get("altura", "").strip()

        # Verificar campos vazios
        if not nome or not peso_str or not altura_str:
            raise ValueError("Por favor, preencha todos os campos: nome, peso e altura.")

        # Tentar converter e validar peso e altura
        try:
            peso = abs(float(peso_str))
            altura = abs(float(altura_str))
        except ValueError:
            raise ValueError("Peso e Altura devem conter valores numéricos válidos.")

        # Validação de peso e altura
        validar_dados(peso, altura)

        # Calcular IMC
        imc = peso / (altura ** 2)
        resultado = f"Olá {nome}, o seu IMC é {imc:.1f} kg/m²."

        # Determinar categoria
        if imc < 18.5:
            categoria = "Abaixo do Peso"
            risco_saude = (
                "Possíveis riscos incluem desnutrição, anemia e imunidade enfraquecida."
            )
            recomendacao_alimentos = """
                Consuma alimentos ricos em calorias saudáveis, como abacate, castanhas e azeite de oliva.
            """
            recomendacao_exercicio = "Pratique atividades de baixo impacto, como yoga ou caminhadas curtas."
            recomendacao_medica = "Consulte um nutricionista para criar um plano alimentar equilibrado."
        elif 18.5 <= imc < 25:
            categoria = "Peso Ideal"
            risco_saude = "Você está saudável! Continue com hábitos equilibrados."
            recomendacao_alimentos = """
                Foque em manter o equilíbrio com alimentos integrais, frutas, vegetais e boas fontes de gordura, como azeite.
            """
            recomendacao_exercicio = (
                "Faça exercícios aeróbicos, musculação leve e alongamentos semanalmente."
            )
            recomendacao_medica = "Realize check-ups regulares para monitorar sua saúde."
        elif 25 <= imc < 30:
            categoria = "Sobrepeso"
            risco_saude = "Risco moderado de hipertensão arterial e diabetes tipo 2."
            recomendacao_alimentos = """
                Reduza açúcares refinados e gorduras saturadas. Priorize vegetais, grãos integrais e proteínas magras.
            """
            recomendacao_exercicio = (
                "Faça caminhadas diárias ou exercícios leves 3-5 vezes por semana."
            )
            recomendacao_medica = "Consulte um profissional de saúde para acompanhamento preventivo."
        elif 30 <= imc < 35:
            categoria = "Obesidade Grau I"
            risco_saude = "Aumento significativo no risco de diabetes e problemas cardiovasculares."
            recomendacao_alimentos = """
                Evite frituras e alimentos ultraprocessados. Priorize vegetais, legumes e refeições menores ao longo do dia.
            """
            recomendacao_exercicio = """
                Comece com atividades físicas de baixo impacto, como natação ou bicicleta ergométrica.
            """
            recomendacao_medica = """
                Um endocrinologista pode ajudar na criação de estratégias seguras para perda de peso.
            """
        elif 35 <= imc < 40:
            categoria = "Obesidade Grau II"
            risco_saude = "Alto risco para doenças graves, como hipertensão severa e doenças metabólicas."
            recomendacao_alimentos = """
                Realize uma mudança alimentar focada no equilíbrio. Hidrate-se e adapte suas refeições para porções menores e saudáveis.
            """
            recomendacao_exercicio = """
                Exercite-se com supervisão especializada, focando em atividades de baixo impacto.
            """
            recomendacao_medica = """
                Procure um endocrinologista e nutricionista para acompanhamento estreito.
            """
        else:
            categoria = "Obesidade Mórbida"
            risco_saude = (
                "Risco extremamente alto para infarto, AVC e complicações devido ao peso elevado."
            )
            recomendacao_alimentos = """
                Controle rigoroso de dieta balanceada: evite açúcares e gorduras saturadas. Hidrate-se adequadamente.
            """
            recomendacao_exercicio = """
                Inicie atividades leves, como caminhadas supervisionadas ou hidroginástica, sempre com acompanhamento profissional.
            """
            recomendacao_medica = """
                Consulta imediata com especialistas (endocrinologista, nutricionista e cardiologista) é recomendada.
            """

        # Salvar o histórico na sessão
        data = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "imc": round(imc, 1),
            "categoria": categoria,
        }
        historico = session.get("historico", [])
        historico.append(data)
        session["historico"] = historico

        # Renderizar resultado
        return render_template(
            "resultado.html",
            resultado=resultado,
            categoria=categoria,
            risco_saude=risco_saude,
            recomendacao_alimentos=recomendacao_alimentos,
            recomendacao_exercicio=recomendacao_exercicio,
            recomendacao_medica=recomendacao_medica,
        )

    except ValueError as e:
        return render_template(
            "index.html",
            erro=str(e),
        )
    except Exception as e:
        # Registrar erro inesperado para depuração
        print(f"[ERRO] Um erro inesperado ocorreu: {e}")
        return render_template(
            "index.html",
            erro="Erro inesperado! Verifique os dados e tente novamente.",
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
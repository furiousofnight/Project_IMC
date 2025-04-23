# Índice de Massa Corporal (IMC)
print("-*-"*20)
print(" "*8,"SEJA BEM-VINDOS! A CALCULADORA IMC FURIOUS!"," "*10)
print("-*-"*20)
nome = str(input("Como você se chama?: ")).strip().capitalize()
print(f"{nome}, vamos precisar de algumas informações para dar continuidade.")
peso = input("Qual seu peso atual? (KG): ")
if not peso.replace('.', '', 1).isdigit():
    print("Por favor, insira um valor numérico válido!")
else:
    peso = float(peso)
    altura = input("Qual sua altura? (M): ")
    if not altura.replace('.', '', 1).isdigit():
        print("Por favor, insira um valor numérico válido!")
    else:
        altura = float(altura)
        imc = peso / (altura ** 2)
        print(f"O seu IMC atual é: {imc:.1f}!")
        if imc < 18.5:
            print("Você está ABAIXO DO PESO normal. O IMC ideal é entre 18.5 e 25.")
        elif 18.5 <= imc < 25:
            print("Você está no PESO IDEAL. Parabéns, continue se cuidando!")
        elif 25 <= imc < 30:
            print("Você está em SOBREPESO. Cuide mais da sua saúde, o IMC ideal é entre 18.5 e 25!")
        elif 30 <= imc < 40:
            print("""Você está em OBESIDADE. Cuide da sua alimentação!
DICAS: O IMC ideal é entre 18.5 e 25.
[1]: Evite comidas gordurosas.
[2]: Evite comer muito açúcar.
[3]: Evite massas em excesso.
[4]: Pratique exercícios físicos com mais frequência.
[5]: Busque acompanhamento médico e de um(a) nutricionista!
Motivação: Cuide mais de você e da sua saúde, pois ninguém vai fazer isso por você!""")
        else:
            print("""Você está em OBESIDADE MÓRBIDA. Este é um caso de EXTREMA ATENÇÃO MÉDICA!
DICAS: O IMC ideal é entre 18.5 e 25.
[1]: Evite comidas gordurosas.
[2]: Evite comer muito açúcar.
[3]: Evite massas em excesso.
[4]: Pratique exercícios físicos com mais frequência.
[5]: Busque acompanhamento médico e de um(a) nutricionista!
Motivação: Cuide mais de você e da sua saúde, pois ninguém vai fazer isso por você!""")
"""  Jogo da Forca
     Feito para o livro -> Introdução a programação com Python 3ªEd
"""

palavra = input('Digite a palavra secreta: ').lower().strip()

for x in range(15):
    print()

dica = input('Dica: ')
digitadas = []
acertos = []
erros = 0

while True:
    senha = ''
    print(palavra)
    print(acertos)
    print(digitadas)
    print(senha)
    for letra in palavra:
        senha += letra if letra in acertos else '_'
    print(senha)

    if senha == palavra:
        print('Você Acertou!')
        break

    tentativa = input('\nDigite uma letra: ').lower().strip()

    if tentativa in digitadas:
        print('Você já tentou esta letra!')
        continue
    else:
        digitadas += tentativa
        if tentativa in palavra:
            acertos += tentativa
        else:
            erros += 1
            print('Você Errou')

    print('====:====')
    print('    O  ' if erros >= 1 else '')

    linha2 = ''
    if erros == 2:
        linha2 = '   | '
    elif erros == 3:
        linha2 = '   \| '
    elif erros >= 4:
        linha2 = '   \|/ '
    print(f'{linha2}')

    linha3 = ''
    if erros == 5:
        linha3 += '   /  '
    elif erros >= 6:
        linha3 += '   / \ '

    print(f'{linha3}')
    print('==========')

    if erros == 6:
        print('Enforcado!')
        print(f'A palavra era: {palavra}')
        break
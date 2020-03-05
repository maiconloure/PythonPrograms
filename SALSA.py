"""Permuta letras de palavras

    Desafio 1:
    >> Máximo que consegui otimizar
    >> Gerar retorno: 'quarta'
    >> var criptada = 'qsueagrutnada'
    >> var salsa = 'segunda'

    Precisa remover 'segunda' dentro de 'qsueagrutnada'
    na ordem exata da palavra. Resultado quarta. """

from itertools import zip_longest


def descriptor(string, salsa):
    """Vai remover salsa."""

    criptada = list(string)
    palavra = []

    for v, i in enumerate(criptada):
        if i in salsa[:1]:
            salsa = salsa[1:]
        else:
            palavra.append(i)

    return ''.join(palavra)


def criptografa(word, salsa):
    """Vai adicionar uma palavra secreta(salsa) na palavra."""

    cripting = (''.join(a + b for a, b in zip_longest(word, salsa, fillvalue='')))

    return cripting


d = criptografa('quarta', 'segunda')
print(d)
print(descriptor(d, 'segunda'))

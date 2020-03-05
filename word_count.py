def contador(string):
    resultado = {}

    for caracter in string:
        resultado[caracter] = (resultado.get(caracter, 0)) + 1

    return resultado


if __name__ == '__main__':
    print(contador('maicon'))
    print(contador('banana'))
    print(contador('lambda'))
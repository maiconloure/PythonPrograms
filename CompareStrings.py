"""Este Programa compara duas strings,
 e verifica os caracteres diferentes na mesma posição."""


def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError("length are not equal")
    else:
        hamming = 0
        for a, b in zip(strand_a, strand_b):
            if a != b:
                hamming += 1

        return hamming


if __name__ == '__main__':
    print(distance('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT'))
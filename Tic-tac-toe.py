m = [1, 2, 3, 4, 5, 6, 7, 8, 9]
m2 = ['', '', '', '', '', '', '', '', '']

jogador = "X"
jogadas = 0

while True:
    if jogadas == 9:
        print('Deu velha, Ninguém ganhou!')
        break

    print(f"""                      Posições
         {m2[0]:1} | {m2[1]:1} | {m2[2]:}    1 | 2 | 3
        ---+---+---  ---+---+---
         {m2[3]:1} | {m2[4]:1} | {m2[5]:1}    4 | 5 | 6
        ---+---+---  ---+---+---
         {m2[6]:1} | {m2[7]:1} | {m2[8]:1}    7 | 8 | 9
         """)

    j = int(input(f'{jogador} - Onde quer Jogar? ').strip())
    if j < 1 or j > 9:
        print('Posição Inválida')
        continue

    if j != m[j - 1]:
        print('Posição Ocupada! Tente novamente.')
        continue

    m[j - 1] = m2[j - 1] = jogador

    if m[0] == m[1] == m[2] or m[0] == m[3] == m[6] or \
            m[3] == m[4] == m[5] or m[1] == m[4] == m[7] or \
            m[6] == m[7] == m[8] or m[2] == m[5] == m[8] or \
            m[0] == m[4] == m[8] or m[2] == m[4] == m[6]:
        print(f'Jogador "{jogador}" Vencedor! ')

        print(f"""                      Posições
             {m2[0]:1} | {m2[1]:1} | {m2[2]:1}    1 | 2 | 3
            ---+---+---  ---+---+---
             {m2[3]:1} | {m2[4]:1} | {m2[5]:1}    4 | 5 | 6
            ---+---+---  ---+---+---
             {m2[6]:1} | {m2[7]:1} | {m2[8]:1}    7 | 8 | 9
             """)
        break

    jogador = 'X' if jogador == 'O' else 'O'
    jogadas += 1
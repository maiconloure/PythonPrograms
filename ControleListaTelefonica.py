agenda = []
agenda2 = []
alterada = False


def pede_nome(default=''):
    name = input('Nome: ')
    if name == '':
        name = default
    return name


def pede_telefone(default=''):
    telephone = input('Telefone: ')
    if telephone == '':
        telephone = default
    return telephone


def pede_nascimento():
    nascimento = input('Data de nascimento: ')
    return nascimento


def pede_email():
    email = input('E-Mail: ')
    return email


def pede_nome_arquivo():
    return input('Nome do arquivo: ')


def mostra_dados(nome, telefone, nascimento, email):
    print(f'Nome: {nome.capitalize():<12} - Telefone: {telefone:<14} - Nascimento: {nascimento:<12} - Email: {email}')


def pesquisa(nome):
    mnome = nome.lower()
    for p, e in enumerate(agenda):
        if e[0].lower() == mnome:
            return p
    return None


def novo():
    global agenda, alterada
    nome = pede_nome()
    if pesquisa(nome) is not None:
        return print(f'Erro. {nome} já está cadastrado na agenda')
    telefone = pede_telefone()
    nascimento = pede_nascimento()
    email = pede_email()
    agenda.append([nome, telefone, nascimento, email])
    alterada = True


def confirma(operacao):
    while True:
        opcao = str(input(f'Confirma - {operacao}?(S/N): ')).upper()
        if opcao in 'SN':
            return opcao
        else:
            print('Resposta Inválida, digite S ou N')


def ultima_agenda():
    global option, agenda2
    if option != 8:
        with open('ultima.txt', 'w', encoding='utf-8') as ultimo:
            for e in agenda:
                ultimo.write(f'{e[0]}#{e[1]}#{e[2]}#{e[3]}\n')
    else:
        with open('ultima.txt', 'r', encoding='utf-8') as ultima:
            agenda2 = []
            for line in ultima.readlines():
                nome, telefone, nascimento, email = line.strip().split('#')
                agenda2.append([nome, telefone, nascimento, email])
        lista(agenda2)


def apaga():
    global agenda, alterada
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:
        if confirma("apagamento") == 'S':
            del agenda[p]
            alterada = True
    else:
        print('Nome não encontrado!')


def altera():
    global alterada
    p = pesquisa(pede_nome())
    if p is not None:
        nome = agenda[p][0]
        telefone = agenda[p][1]
        nascimento = agenda[p][2]
        email = agenda[p][3]
        print('Encontrado: ')
        mostra_dados(nome, telefone, nascimento, email)
        nome = pede_nome()
        telefone = pede_telefone()
        if confirma("alteraração") == 'S':
            agenda[p] = [nome, telefone, nascimento, email]
            alterada = True
    else:
        print('Nome não encontrado')


def lista(arquivo=None):
    if arquivo is None:
        arquivo = agenda
    print("\nAgenda\n--------")
    for posicao, e in enumerate(arquivo):
        print(f'Nº 0{posicao + 1} = ', end='')
        mostra_dados(e[0], e[1], e[2], e[3])
    print("-" * 15)


def leitura():
    global agenda, alterada
    if alterada:
        print("Você não salvou a lista desde a última alteração. Deseja gravá-la agora?")
        if confirma('gravação') == 'S':
            grava()
    nome_arquivo = pede_nome_arquivo()
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            agenda = []
            for l in arquivo.readlines():
                nome, telefone, nascimento, email = l.strip().split('#')
                agenda.append([nome, telefone, nascimento, email])
    except FileNotFoundError:
        print('Arquivo não existe!')
    ultima_agenda()
    alterada = False


def ordenar():
    global alterada
    agenda.sort(key=lambda e: e[0])
    alterada = True


def grava():
    global alterada
    if not alterada:
        print('Você não alterou a lista. Deseja gravá-la mesmo assim?')
        if confirma('Gravação') == 'N':
            return
    print('Gravar\n------------')
    nome_arquivo = pede_nome_arquivo()
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        for e in agenda:
            arquivo.write(f'{e[0]}#{e[1]}#{e[2]}#{e[3]}\n')
    ultima_agenda()


def valida_faixa_inteiro(pergunta, min, max):
    while True:
        try:
            op = int(input(pergunta))
            if min <= op <= max:
                return op
        except ValueError:
            print(f'Valor Inválido, digite um valor entre {min} e {max}')


def menu():
    print("""\nControle de agendas de telefone\n
    1 - Novo
    2 - Altera
    3 - Apaga
    4 - Lista
    5 - Grava
    6 - Lê 
    7 - Ordernar por nome
    8 - Ultima lista
    0 - Sair
""")
    alt = 'Sim' if alterada else 'Não'
    print(f'Nomes na agenda: {len(agenda)} - Alterada: {alt}')
    print('-' * 17)
    return valida_faixa_inteiro("Escolha uma opção: ", 0, 8)


while True:
    option = menu()
    if option == 0:
        break
    elif option == 1:
        novo()
    elif option == 2:
        altera()
    elif option == 3:
        apaga()
    elif option == 4:
        lista()
    elif option == 5:
        grava()
    elif option == 6:
        leitura()
    elif option == 7:
        ordenar()
    elif option == 8:
        ultima_agenda()

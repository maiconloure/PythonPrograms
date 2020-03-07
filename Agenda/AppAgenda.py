import sys
import pickle
from functools import total_ordering
from AgendaFinal.DBagenda import *


def nulo_ou_vazio(texto):
    return texto is None or not texto.strip()


def valida_faixa_inteiro(pergunta, inicio, fim, padrao=None):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada) and padrao is not None:
                entrada = padrao
            valor = int(entrada)
            if inicio <= valor <= fim:
                return valor
        except ValueError:
            print(f"Valor inválido, favor digitar entre {inicio} e {fim}")


def valida_faixa_inteiro_ou_branco(pergunta, inicio, fim):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada):
                return None
            valor = int(entrada)
            if inicio <= valor <= fim:
                return valor
        except ValueError:
            print(f"Valor inválido, favor digite entre {inicio} e {fim}")


class ListaUnica:
    def __init__(self, elem_class):
        self.lista = []
        self.elem_class = elem_class

    def __len__(self):
        return len(self.lista)

    def __iter__(self):
        return iter(self.lista)

    def __getitem__(self, p):
        return self.lista[p]

    def IndiceValido(self, i):
        return 0 <= i < len(self.lista)

    def adiciona(self, elem):
        if self.pesquisa(elem) == -1:
            self.lista.append(elem)

    def remove(self, elem):
        self.lista.remove(elem)

    def pesquisa(self, elem):
        self.verifica_tipo(elem)
        try:
            return self.lista.index(elem)
        except ValueError:
            return -1

    def verifica_tipo(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError("Tipo Inválido")

    def ordena(self, chave=None):
        self.lista.sort(key=chave)


@total_ordering
class Nome:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Class {type(self).__name__} in 0x{id(self):x} Name: {self.name} Key: {self.__key}>"

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if nulo_ou_vazio(value):
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.__name = value
        self.__key = Nome.CriaChave(value)

    @property
    def key(self):
        return self.__key

    @staticmethod
    def CriaChave(name):
        return name.strip().lower()


@total_ordering
class TipoTelefone:
    def __init__(self, tipo):
        self.tipo = tipo

    def __str__(self):
        return f"({self.tipo})"

    def __eq__(self, outro):
        if outro is None:
            return False
        return self.tipo == outro.tipo

    def __lt__(self, outro):
        return self.tipo < outro.tipo


class Telefone:
    def __init__(self, numero, tipo=None):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        if self.tipo is not None:
            tipo = self.tipo
        else:
            tipo = ""
        return f"{self.numero} {tipo}"

    def __eq__(self, other):
        return self.numero == other.numero and ((self.tipo == other.tipo) or (self.tipo is None or other.tipo is None))

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, value):
        if value is None or not value.strip():
            raise ValueError('Numero não pode ser Nulo ou em branco')
        self.__numero = value


class Telefones(ListaUnica):
    def __init__(self):
        super().__init__(Telefone)


class TiposTelefone(ListaUnica):
    def __init__(self):
        super().__init__(TipoTelefone)


class DadoAgenda(object):
    def __init__(self, nome):
        self.nome = nome
        self.telefones = Telefones()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, Nome):
            raise TypeError("nome deve ser um instância da classe Nome")
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posicao = self.telefones.pesquisa(Telefone(telefone))
        if posicao == -1:
            return None
        else:
            return self.telefones[posicao]


class Agenda(ListaUnica):
    def __init__(self):
        super().__init__(DadoAgenda)
        self.tiposTelefone = TiposTelefone()

    def adicionaTipo(self, tipo):
        self.tiposTelefone.adiciona(TipoTelefone(tipo))

    def pesquisaNome(self, nome):
        if isinstance(nome, str):
            nome = Nome(nome)
        for dados in self.lista:
            if dados.nome == nome:
                return dados
        else:
            return None

    def ordena(self, **kwargs):
        super().ordena(lambda dado: str(dado.nome))


class Menu:
    def __init__(self):
        self.opcoes = [['Sair', None]]

    def adicionaOpcao(self, nome, funcao):
        self.opcoes.append([nome, funcao])

    def exibe(self):
        print('='*16)
        print('MENU'.center(16))
        print('='*16)
        for i, opcao in enumerate(self.opcoes):
            print(f'[{i}] - {opcao[0]}')
        print()

    def execute(self):
        while True:
            self.exibe()
            escolha = valida_faixa_inteiro("Escolha uma Opção: ", 0, len(self.opcoes)-1)
            if escolha == 0:
                break
            self.opcoes[escolha][1]()  # self.opcoes[1][1]() ->


class AppAgenda:
    @staticmethod
    def pede_nome():
        return input("Nome: ")

    @staticmethod
    def pede_telefone():
        return input("Telefone: ")

    @staticmethod
    def mostra_dados(dados):
        print(f'Nome: {dados.nome}')
        for telefone in dados.telefones:
            print(f'Telefone: {telefone}')
        print()

    @staticmethod
    def mostra_dados_telefone(dados):
        print(f'Nome: {dados.nome}')
        for i, telefone in enumerate(dados.telefones):
            print(f'{i} - Telefone: {telefone}')
        print()

    def __init__(self, banco):
        self.agenda = DBAgenda(banco)
        self.menu = Menu()
        self.menu.adicionaOpcao("Novo", self.novo)
        self.menu.adicionaOpcao("Altera", self.altera)
        self.menu.adicionaOpcao("Apaga", self.apaga)
        self.menu.adicionaOpcao("Lista", self.lista)
        self.ultimo_nome = None

    def pede_tipo_telefone(self, padrao=None):
        for i, tipo in enumerate(self.agenda.tiposTelefone):
            print(f' {i} - {tipo} ', end="")
        t = valida_faixa_inteiro("Tipo: ", 0, len(self.agenda.tiposTelefone) - 1, padrao)
        return self.agenda.tiposTelefone[t]

    def pesquisa(self, nome):
        dado = self.agenda.pesquisaNome(nome)
        return dado

    def novo(self):
        novo = AppAgenda.pede_nome()
        if nulo_ou_vazio(novo):
            return
        nome = Nome(novo)
        if self.pesquisa(nome) is not None:
            print("Nome já Existe!")
            return
        registro = DadoAgenda(nome)
        self.menu_telefones(registro)
        self.agenda.adiciona(registro)

    def apaga(self):
        if len(self.agenda) == 0:
            print("Agenda Vazia, nada a apagar")
        nome = AppAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            self.agenda.remove(p)
            print(f'Apagado. A agenda agora possui apenas: {len(self.agenda)} Registros')
        else:
            print("Nome não encontrado.")

    def altera(self):
        if len(self.agenda) == 0:
            print("Agenda vazia, nada a alterar")
        nome = AppAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            print("\nEncontrado:\n")
            AppAgenda.mostra_dados(p)
            print("Digite enter caso não queira alterar o nome")
            novo = AppAgenda.pede_nome()
            if not nulo_ou_vazio(novo):
                p.nome = Nome(novo)
            self.menu_telefones(p)
        else:
            print("Nome não encontrado!")

    def menu_telefones(self, dados):
        while True:
            print("\nEditando telefones")
            AppAgenda.mostra_dados(dados)
            if len(dados.telefones) > 0:
                print("\n[A] -  alterar\n[D] - apagar\n", end="")
            print("[N] - novo\n[S] - sair\n")
            operacao = input("Escolha uma Operação: ")
            operacao = operacao.lower()
            if operacao not in ['a', 'd', 'n', 's']:
                print("Operação inválida. Digite A, D, N ou S")
                continue
            if operacao == 'a' and len(dados.telefones) > 0:
                self.altera_telefones(dados)
            elif operacao == 'd' and len(dados.telefones) > 0:
                self.apaga_telefone(dados)
            elif operacao == 'n':
                self.novo_telefone(dados)
            elif operacao == 's':
                break

    def novo_telefone(self, dados):
        telefone = AppAgenda.pede_telefone()
        if nulo_ou_vazio(telefone):
            return
        if dados.pesquisaTelefone(telefone) is not None:
            print("Telefone já existe")
        tipo = self.pede_tipo_telefone()
        dados.telefones.adiciona(Telefone(telefone, tipo))

    @staticmethod  # ALTERADA@@@
    def apaga_telefone(dados):
        t = valida_faixa_inteiro_ou_branco(
            "Digite a posição do número a apagar, enter para sair: ", 0, len(dados.telefones) - 1)
        if t is None:
            return
        dados.telefones.remove(dados.telefones[t])

    def altera_telefones(self, dados):
        t = valida_faixa_inteiro_ou_branco(
            "Digite a posição do número a alterar. enter para sair: ", 0, len(dados.telefones) - 1)
        if t is None:
            return
        telefone = dados.telefones[t]
        print(f'Telefone: {telefone}')
        print("Digite enter caso não queria alterar o número")
        novotelefone = AppAgenda.pede_telefone()
        if not nulo_ou_vazio(novotelefone):
            telefone.numero = novotelefone
        print("Digite enter caso não queria alterar o tipo")
        telefone.tipo = self.pede_tipo_telefone(
            self.agenda.tiposTelefone.pesquisa(telefone.tipo))

    def lista(self):
        print("\nAgenda")
        print("-" * 60)
        for e in self.agenda:
            AppAgenda.mostra_dados(e)
        print("-" * 60)

    def le(self, nome_arquivo=None):
        if nome_arquivo is None:
            nome_arquivo = AppAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            return
        with open(nome_arquivo, "rb") as arquivo:
            self.agenda = pickle.load(arquivo)
        self.ultimo_nome = nome_arquivo

    def ordena(self):
        self.agenda.ordena()
        print("\nAgenda ordenada\n")

    def grava(self):
        if self.ultimo_nome is not None:
            print(f"Último nome utilizado foi '{self.ultimo_nome}'")
            print("Digite enter caso queira utilizar o mesmo nome")
        nome_arquivo = AppAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            if self.ultimo_nome is not None:
                nome_arquivo = self.ultimo_nome
            else:
                return
        with open(nome_arquivo, "wb") as arquivo:
            pickle.dump(self.agenda, arquivo)

    def execute(self):
        self.menu.execute()


if __name__ == "__main__":
    app = AppAgenda()
    if len(sys.argv) > 1:
        app.le(sys.argv[1])
    app.execute()

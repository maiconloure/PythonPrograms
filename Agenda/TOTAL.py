import sys
import sqlite3
import os.path
from functools import total_ordering


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


class DBListaUnica(ListaUnica):
    def __init__(self, elem_class):
        super().__init__(elem_class)
        self.apagados = []

    def remove(self, elem):
        if elem.id is not None:
            self.apagados.append(elem.id)
        super().remove(elem)

    def limpa(self):
        self.apagados = []


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


class DBNome(Nome):
    def __init__(self, nome, id_=None):
        super().__init__(nome)
        self.id = id_


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


class DBTipoTelefone(TipoTelefone):
    def __init__(self, id_, tipo):
        super().__init__(tipo)
        self.id = id_


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


class DBTelefone(Telefone):
    def __init__(self, numero, tipo=None, id_=None, id_nome=None):
        super().__init__(numero, tipo)
        self.id = id_
        self.id_nome = id_nome


class DBTelefones(DBListaUnica):
    def __init__(self):
        super().__init__(DBTelefone)


class DBTiposTelefone(ListaUnica):
    def __init__(self):
        super().__init__(DBTipoTelefone)


class DBDadoAgenda:
    def __init__(self, nome):
        self.nome = nome
        self.telefones = DBTelefones()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(type(valor), DBNome):
            raise TypeError("Nome deve ser uma instância da classe DBNome")
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posicao = self.telefones.pesquisa(DBTelefone(telefone))
        if posicao == -1:
            return None
        else:
            return self.telefones[posicao]


class DBAgenda:
    def __init(self, banco):
        self.tiposTelefone = DBTiposTelefone()
        self.banco = banco
        self.conexao = sqlite3.connect(banco)   # fazendo a conexão
        self.conexao.row_factory = sqlite3.Row  # acessar as tabelas pelo nome(chave), como um dicionario
        novo = not os.path.isfile(banco)  # verificando se o banco de dados já existe

        if novo:
            self.cria_banco()

        self.carrega_tipos()

    def carrega_tipos(self):  # realiza a leitura de todos os tipos de telefone e guarda na  lista 'tiposTelefone'
        for tipo in self.conexao.execute("select * from tipos"):
            id_ = tipo["id"]
            descricao = tipo['descricao']
            print(f'(carrega_tipos) -> id: {id_} descricao: {descricao}')  # @@@@@@
            self.tiposTelefone.adiciona(DBTipoTelefone(id_, descricao))  # guardando 'id', e o tipo

    def cria_banco(self):
        self.conexao.executescript(BANCO)  # executa varios comandos de uma vez, só é possivel pq sao separados por ;

    def pesquisa_nome(self, nome):
        if not isinstance(nome, DBNome):
            raise TypeError("nome deve ser do tipo DBNome")

        achado = self.conexao.execute("select count(*) from nomes where nome = ?", (nome.nome,)).fetchone()
        print(f'(pesquisa_nome) -> achado: {achado}')
        if achado[0] > 0:
            return self.carrega_por_nome(nome)
        else:
            return None

    def carrega_por_id(self, id):
        consulta = self.conexao.execute("select * from nomes where id = ?", (id,))
        print(f'(carrega_por_id) consulta: {consulta}')  # @@@@@@
        return self.carrega(consulta.fetchone())

    def carrega_por_nome(self, nome):
        consulta = self.conexao.execute("select * from nomes where nome = ?", (nome.nome, ))
        print(f'(carrega_por_nome) consulta: {consulta}')  # @@@@@@
        return self.carrega(consulta.fetchone())

    def carrega(self, consulta):
        if consulta is None:
            return None

        novo = DBDadoAgenda(DBNome(consulta["nome"], consulta["id"]))
        print(f'(carrega)> novo: {novo}')  # @@@@@@

        for telefone in self.conexao.execute("select * from telefones where id_nome = ?", (nome.nome.id, )):
            ntel = DBTelefone(telefone["numero"], None, telefone["id"], telefone["id_nome"])
            print(f'(carrega)> ntel: {ntel}')  # @@@@@@

            for tipo in self.tiposTelefone:
                if tipo.id == telefone["id_tipo"]:
                    ntel.tipo = tipo
                    break
            novo.telefones.adiciona(ntel)
        print(f'(carega) -> novo: {novo}')  # @@@@@@
        return novo

    def lista(self):
        consulta = self.conexao.execute("select * from nomes order by nome")
        print(f'(list) -> consulta: {consulta}')  # @@@@@@
        for registro in consulta:
            yield self.carrega(registro)

    def novo(self, registro):
        try:
            cur = self.conexao.cursor()
            cur.execute("insert into nomes(nome) values (?)", (str(registro.nome),))
            registro.nome.id = cur.lastrowid
            print(f'(novo) -> registro.nome.id: {registro.nome.id} /lastrowid/')  # @@@@@@

            for telefone in registro.telefones:
                cur.execute("""insert into telefones(numero, id_tipo, id_nome) values (?,?,?)""",
                            (telefone.numero, telefone.tipo.id, registro.nome.id))
                telefone.id = cur.lastrowid
            self.conexao.commit()

        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def atualiza(self, registro):
        try:
            cur = self.conexao.cursor()
            cur.execute("update nomes set nome=? where id = ?",
                        (str(registro.nome), registro.nome.id))

            for telefone in registro.telefones:
                print(f'(atualiza) -> try > telefone: {telefone}')  # @@@@@@
                if telefone.id is None:
                    cur.execute("""insert into telefones(numero, id_tipo, id_nome) values (?,?,?)""",
                                (telefone.numero, telefone.tipo.id, registro.nome.id))
                    telefone.id = cur.lastrowid

                else:
                    cur.execute("""update telefones set numero=?, id_tipo=?, id_nome=? where id = ?""",
                                (telefone.numero, telefone.tipo.id, registro.nome.id, telefone.id))

            for apagado in registro.telefones.apagados:
                cur.execute("delete from telefones where id = ?", (apagado,))

            self.conexao.commit()
            registro.telefones.limpa()

        except Exception:
            self.conexao.rollback()
            raise

        finally:
            cur.close()

    def apaga(self, registro):
        try:
            cur = self.conexao.cursor()
            cur.execute("delete from telefones where id_nome = ?", (registro.nome.id,))
            cur.execute("delete from nomes where id = ?", (registro.nome.id,))
            self.conexao.commit()

        except Exception:
            self.conexao.rollback()
            raise

        finally:
            cur.close()


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

    @staticmethod
    def pede_nome_arquivo():
        return input("Nome do arquivo: ")

    def __init__(self):
        self.agenda = Agenda()
        self.agenda.adicionaTipo("Celular")
        self.agenda.adicionaTipo("Residencial")
        self.agenda.adicionaTipo("Trabalho")
        self.agenda.adicionaTipo("Fax")
        self.menu = Menu()
        self.menu.adicionaOpcao("Novo", self.novo)
        self.menu.adicionaOpcao("Altera", self.altera)
        self.menu.adicionaOpcao("Apaga", self.apaga)
        self.menu.adicionaOpcao("Lista", self.lista)
        self.menu.adicionaOpcao("Grava", self.grava)
        self.menu.adicionaOpcao("Lê", self.le)
        self.menu.adicionaOpcao("Ordena", self.ordena)
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
    if len(sys.argv) > 1:
        app = AppAgenda(sys.argv[1])
        app.execute()
    else:
        print("Erro: nome do banco de dados não informado")
        print("agenda.py nome_do_banco")




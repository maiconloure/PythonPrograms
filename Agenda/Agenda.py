from functools import total_ordering
import os.path
import sqlite3

BANCO = """
create table tipos(id integer primary key autoincrement,
                    descricao text);
create table nomes(id integer primary key autoincrement,
                    nome text);
create table telefones(id integer primary key autoincrement,
                    id_nome integer,
                    numero text,
                    id_tipo integer);
insert into tipos(descricao) values ("Celular");
insert into tipos(descricao) values ("Fixo");
insert into tipos(descricao) values ("Fax");
insert into tipos(descricao) values ("Casa");
insert into tipos(descricao) values ("Trabalho");
"""

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
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"<Class {type(self).__name__} in 0x{id(self):x} Name: {self.nome} Key: {self.__chave}>"

    def __eq__(self, other):
        return self.nome == other.nome

    def __lt__(self, other):
        return self.nome < other.nome

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if nulo_ou_vazio(valor):
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.__nome = valor
        self.__chave = Nome.CriaChave(valor)

    @property
    def key(self):
        return self.__chave

    @staticmethod
    def CriaChave(nome):
        return nome.strip().lower()


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

    def __eq__(self, outro):
        return self.numero == outro.numero and (
               (self.tipo == outro.tipo) or (
                self.tipo is None or outro.tipo is None))

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor):
        if nulo_ou_vazio(valor):
            raise ValueError("Número não pode ser None ou em branco")
        self.__numero = valor


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
        if not isinstance(valor, DBNome):
            raise TypeError("Nome deve ser uma instância da classe DBNome")
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posicao = self.telefones.pesquisa(DBTelefone(telefone))
        if posicao == -1:
            return None
        else:
            return self.telefones[posicao]


class DBAgenda:
    def __init__(self, banco):
        self.tiposTelefone = DBTiposTelefone()
        self.banco = banco
        novo = not os.path.isfile(banco)
        self.conexao = sqlite3.connect(banco)
        self.conexao.row_factory = sqlite3.Row
        if novo:
            self.cria_banco()
        self.carrega_tipos()

    def cria_banco(self):
        self.conexao.executescript(BANCO)

    def carrega_tipos(self):
        for tipo in self.conexao.execute("select * from tipos"):
            id_ = tipo["id"]
            descricao = tipo['descricao']
            self.tiposTelefone.adiciona(DBTipoTelefone(id_, descricao))

    def pesquisa_nome(self, nome):
        if not isinstance(nome, DBNome):
            raise TypeError("nome deve ser do tipo DBNome")
        achado = self.conexao.execute("""select count(*) from nomes where nome = ?""", (nome.nome,)).fetchone()
        if achado[0] > 0:
            return self.carrega_por_nome(nome)
        else:
            return None

    def carrega_por_id(self, id):
        consulta = self.conexao.execute("select * from nomes where id = ?", (id,))
        return self.carrega(consulta.fetchone())

    def carrega_por_nome(self, nome):
        consulta = self.conexao.execute("select * from nomes where nome = ?", (nome.nome, ))
        return self.carrega(consulta.fetchone())

    def carrega(self, consulta):
        if consulta is None:
            return None
        novo = DBDadoAgenda(DBNome(consulta["nome"], consulta["id"]))
        for telefone in self.conexao.execute("select * from telefones where id_nome = ?", (novo.nome.id,)):
            ntel = DBTelefone(telefone["numero"], None, telefone["id"], telefone["id_nome"])
            for tipo in self.tiposTelefone:
                if tipo.id == telefone["id_tipo"]:
                    ntel.tipo = tipo
                    break
            novo.telefones.adiciona(ntel)
        return novo

    def lista(self):
        consulta = self.conexao.execute("select * from nomes order by nome")
        for registro in consulta:
            yield self.carrega(registro)

    def novo(self, registro):
        cur = None
        try:
            cur = self.conexao.cursor()
            cur.execute("insert into nomes(nome) values (?)", (str(registro.nome),))
            registro.nome.id = cur.lastrowid
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
        cur = None
        try:
            cur = self.conexao.cursor()
            cur.execute("update nomes set nome=? where id = ?",
                        (str(registro.nome), registro.nome.id))
            for telefone in registro.telefones:
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
        cur = None
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
            self.opcoes[escolha][1]()  # self.opcoes[4][1]() -> self.lista()


class AppAgenda:
    @staticmethod
    def pede_nome():
        return input("Nome: ")

    @staticmethod
    def pede_telefone():
        return input("Telefone: ")

    @staticmethod
    def mostra_dados(dados):
        print(f"Nome: {dados.nome}")
        for telefone in dados.telefones:
            print(f"Telefone: {telefone}")
        print()

    @staticmethod
    def mostra_dados_telefone(dados):
        print(f"Nome: {dados.nome}")
        for i, telefone in enumerate(dados.telefones):
            print(f"{i} - Telefone: {telefone}")
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
            print(f" {i} - {tipo} ", end=None)
        t = valida_faixa_inteiro(
            "Tipo: ", 0,
            len(self.agenda.tiposTelefone)-1, padrao)
        return self.agenda.tiposTelefone[t]

    def pesquisa(self, nome):
        if isinstance(nome, str):
            nome = DBNome(nome)
        dado = self.agenda.pesquisa_nome(nome)
        return dado

    def novo(self):
        novo = AppAgenda.pede_nome()
        if nulo_ou_vazio(novo):
            return
        nome = DBNome(novo)
        if self.pesquisa(nome) is not None:
            print("Nome já existe!")
            return
        registro = DBDadoAgenda(nome)
        self.menu_telefones(registro)
        self.agenda.novo(registro)

    def apaga(self):
        nome = AppAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            self.agenda.apaga(p)
        else:
            print("Nome não encontrado.")

    def altera(self):
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
                p.nome.nome = novo
            self.menu_telefones(p)
            self.agenda.atualiza(p)
        else:
            print("Nome não encontrado!")

    def menu_telefones(self, dados):
        while True:
            print("\nEditando telefones\n")
            AppAgenda.mostra_dados_telefone(dados)
            if len(dados.telefones) > 0:
                print("\n[A] - alterar\n[D] - apagar\n", end="")
            print("[N] - novo\n[S] - sair\n")
            operation = input("Escolha uma operação: ")
            operation = operation.lower()
            if operation not in ["a", "d", "n", "s"]:
                print("Operação inválida. Digite A, D, N ou S")
                continue
            if operation == 'a' and len(dados.telefones) > 0:
                self.altera_telefones(dados)
            elif operation == 'd' and len(dados.telefones) > 0:
                self.apaga_telefone(dados)
            elif operation == 'n':
                self.novo_telefone(dados)
            elif operation == "s":
                break

    def novo_telefone(self, dados):
        telefone = AppAgenda.pede_telefone()
        if nulo_ou_vazio(telefone):
            return
        if dados.pesquisaTelefone(telefone) is not None:
            print("Telefone já existe")
        tipo = self.pede_tipo_telefone()
        dados.telefones.adiciona(DBTelefone(telefone, tipo))

    @staticmethod
    def apaga_telefone(dados):
        t = valida_faixa_inteiro_ou_branco(
            "Digite a posição do número a apagar, enter para sair: ", 0, len(dados.telefones)-1)
        if t is None:
            return
        dados.telefones.remove(dados.telefones[t])

    def altera_telefones(self, dados):
        t = valida_faixa_inteiro_ou_branco(
            "Digite a posição do número a alterar, enter para sair: ", 0, len(dados.telefones)-1)
        if t is None:
            return
        telefone = dados.telefones[t]
        print(f"Telefone: {telefone}")
        print("Digite enter caso não queira alterar o número")
        novotelefone = AppAgenda.pede_telefone()
        if not nulo_ou_vazio(novotelefone):
            telefone.numero = novotelefone
        print("Digite enter caso não queira alterar o tipo")
        telefone.tipo = self.pede_tipo_telefone(
            self.agenda.tiposTelefone.pesquisa(telefone.tipo))

    def lista(self):
        print("\nAgenda")
        print("-" * 60)
        for e in self.agenda.lista():
            AppAgenda.mostra_dados(e)
        print("-" * 60)

    def execute(self):
        self.menu.execute()


if __name__ == "__main__":
    app = AppAgenda('agenda.db')
    app.execute()
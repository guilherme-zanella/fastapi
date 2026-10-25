from sqlalchemy import create_engine, Integer, String, Boolean, Float, Column, ForeignKey, Enum
from sqlalchemy.orm import declarative_base

#Cria a conexão do seu banco
db = create_engine('sqlite:///banco.db')

# Cria a base do banco de dados
Base = declarative_base()

# Cria as clsses/tabelas do banco
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable=False)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean, default=True)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    status = Column('status', Enum('pendente', 'cancelado', 'finalizado'))
    dono = Column('dono', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)
    #itens = 

    def __init__(self, dono, status='pendente', preco=0):
        self.dono = dono
        self.status = status
        self.preco = preco



class Itens(Base):
    __tablename__ = 'itens'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco_unitario', Float)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

    def __init__(self, sabor, tamanho, preco_unitario, pedido, quantidade=1):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

# Executa a criação dos metadados do seu banco (cria efetivamente o banco)


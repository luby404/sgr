from peewee import (
    CharField,
    TextField,
    DecimalField,
    IntegerField,
    BooleanField,
    DateTimeField,
    ForeignKeyField
)
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .settings import db, BaseModel


class Usuarios(BaseModel, UserMixin):
    nome  = CharField(unique=True)
    email = CharField(unique=True)
    senha = CharField()

    user_type = CharField(
        choices=[
            ("admin", "admin"),
            ("gestor", "gestor"),
            ("financas", "financas"),
            ("estoquista", "estoquista"),
            ("vendedor", "vendedor")
        ],
        default="vendedor"
    )

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def __str__(self):
        return self.email


class Categorias(BaseModel):
    nome = CharField(unique=True)

    def __str__(self):
        return self.nome


class Produtos(BaseModel):
    categoria      = ForeignKeyField(Categorias, backref="produtos")
    nome           = CharField(unique=True)
    quantidade     = IntegerField(default=0)
    preco_venda    = DecimalField(max_digits=16, decimal_places=2, default=0)
    estoque_minimo = IntegerField(default=10)
    capa_produto   = CharField(max_length=300, null=True)

    def __str__(self):
        return self.nome

class Fornecedor(BaseModel):
    nome     = CharField(unique=True)
    telefone = CharField(unique=True)

    def __str__(self):
        return self.nome

class Estoque(BaseModel):
    produto      = ForeignKeyField(Produtos, backref="movimentos")
    fornecedor   = ForeignKeyField(Fornecedor, backref="movimentos", null=True)

    preco_compra = DecimalField(max_digits=16, decimal_places=2, default=0)
    quantidade   = IntegerField()

    movimento = CharField(
        choices=[
            ("entrada", "entrada"),
            ("saida", "saida"),
            ("ajuste", "ajuste")
        ]
    )

    nota = TextField(null=True)
    data = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.produto.nome} - {self.movimento} ({self.quantidade})"

class Mesa(BaseModel):
    numero = IntegerField(unique=True)
    status = CharField(
        choices=[
            ("livre", "livre"),
            ("ocupada", "ocupada"),
            ("manutencao", "manutencao")
        ],
        default="livre"
    )

    def __str__(self):
        return f"Mesa {self.numero}"

class Comanda(BaseModel):
    mesa   = ForeignKeyField(Mesa, backref="comandas", null=True)
    codigo = IntegerField()
    status = CharField(
        choices=[
            ("aberta", "aberta"),
            ("fechada", "fechada"),
        ],
        default="aberta"
    )

    #aberta_em = DateTimeField(default=datetime.now)
    #fechada_em = DateTimeField(null=True)

    def __str__(self):
        return f"Comanda #{self.codigo}"

class Pedido(BaseModel):
    comanda   = ForeignKeyField(Comanda, backref="pedidos")
    produtos  = IntegerField(default=0)
    sub_total = DecimalField(max_digits=16, decimal_places=2, default=0)
    
    status  = CharField(
        choices=[
            ("pendente", "pendente"),
            ("cancelado", "cancelado"),
            ("finalizado", "finalizado")
        ],
        default="pendente"
    )

    nota       = TextField(null=True)
    aberto_em  = DateTimeField(default=datetime.now)
    fechado_em = DateTimeField(null=True)
    

    def __str__(self):
        return f"Pedido {self.id} - {self.status}"

class ItemPedido(BaseModel):
    pedido     = ForeignKeyField(Pedido, backref="itens")
    produto    = ForeignKeyField(Produtos)
    quantidade = IntegerField()
    preco      = DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"

class Caixa(BaseModel):
    nome   = CharField(unique=True)
    status = BooleanField(default=False)

    saldo_inicial = DecimalField(max_digits=16, decimal_places=2)
    saldo_atual   = DecimalField(max_digits=16, decimal_places=2)

    aberto_em     = DateTimeField(null=True)
    fechado_em    = DateTimeField(null=True)

    def __str__(self):
        return self.nome

class Venda(BaseModel):
    caixa    = ForeignKeyField(Caixa,    null=True, backref="vendas")
    vendedor = ForeignKeyField(Usuarios, null=True, backref="vendas")
    pedido   = ForeignKeyField(Pedido,   backref="vendas")

    valor    = DecimalField(max_digits=16, decimal_places=2)
    data     = DateTimeField(default=datetime.now)

class Settings(BaseModel):
    nome = CharField(unique=True)
    nif  = CharField(unique=True)
    logo = CharField(null=True)
    taxa = DecimalField(max_digits=16, decimal_places=2)
    descricao = TextField(null=True)


def init_models():
    db.connect()
    with db:
        db.create_tables([
            Usuarios, Categorias, Produtos, Fornecedor,
            Estoque, Mesa, Comanda,
            Pedido, ItemPedido,
            Caixa, Venda, Settings
        ])
        
        try:
            Usuarios.create(
                nome="Admin", 
                email="ricardokayoca@gmail.com",
                senha=generate_password_hash("admin"),
                user_type="admin"
            )
        except:
            ...







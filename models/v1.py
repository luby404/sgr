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
            ("finanças", "finanças"),
            ("estoquista", "estoquista")
        ],
        default="vendedor"
    )

    def set_password(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_password(self, senha:str):
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
    # o preço deve ser atualizado assim que o preço do estoque for alterado
    price_venda    = DecimalField(max_digits=16, default=0, decimal_places=2)
    
    estoque_minimo = IntegerField(default=10)
    capa_produto   = CharField(max_length=300, null=True)
    #controle_estoque = BooleanField(default=True, help_text="Esse produto deve ter controle de estoqe?")


    def __str__(self):
        return self.nome

class Fornecedor(BaseModel):
    nome     = CharField(unique=True)
    telefone = CharField(unique=True)
    def __str__(self):
        return self.nome

class Estoque(BaseModel):
    produto      = ForeignKeyField(Produtos, backref="estoque")
    fornecedor   = ForeignKeyField(Fornecedor, backref="estoque")

    preco_compra = DecimalField(max_digits=16, null=True, default=0, decimal_places=2, verbose_name="Preço unitario")
    preco_venda  = DecimalField(max_digits=16, null=True, default=0, decimal_places=2, verbose_name="Preço de venda")
    quantidade   = IntegerField(default=0)

    movimento = CharField(
        choices=[
            ("entrada", "entrada"),
            ("saida", "saida"),
            ("ajuste", "ajuste")
        ]
    )

    nota = TextField(null=True, verbose_name="Nota da Movimentação")
    def __str__(self):
        return f"produto: {self.produto.nome} tipo:{self.movimento} quantidade:{self.quantidade}"

class Cliente(BaseModel):
    """ Mesa ou comanda """
    nome = CharField(unique=True)
    tipo = CharField(
        choices=[
            ("mesa", "mesa"),
            ("comanda", "comanda")
        ]
    )
    status = CharField(
        choices=[
            ("aberta", "aberta"),
            ("fechada", "fechada"),
            ("em manutenção", "em manutenção")
        ]
    )

    def __str__(self):
        return self.nome

class Pedidos(BaseModel):
    cliente = ForeignKeyField(Cliente, backref="pedidos")
    status  = CharField(
        choices=[
            ("pendente", "pendente"),
            ("em preparação", "em preparação"),
            ("enviado", "enviado"),
            ("finalizado", "finalizado"),
        ]
    )

    nota = TextField(null=True)

    def __str__(self):
        return f"{self.cliente.nome} -> {self.status}"
    
class ItenPedido(BaseModel):
    pedito     = ForeignKeyField(Pedidos, backref="produtos")
    produto    = ForeignKeyField(Produtos, backref="produto")
    quantidade = IntegerField()
    price      = DecimalField(decimal_places=2, max_digits=16)

class Caixa(BaseModel):
    nome   = CharField(unique=True)
    status = BooleanField(default=False)

    saldo_inicial = DecimalField(decimal_places=2, max_digits=16)
    saldo_atual   = DecimalField(decimal_places=2, max_digits=16)

    data_open     = DateTimeField(null=True)
    data_close    = DateTimeField(null=True)

class Vendas(BaseModel):
    caixa    = ForeignKeyField(Caixa, backref="vendas")
    vendedor = ForeignKeyField(Usuarios, backref="vendas")
    pedido   = ForeignKeyField(Pedidos, backref="vendas")

    valor    = DecimalField(decimal_places=2, max_digits=16)

# informações do estabelecimento
class Settings(BaseModel):
    nome = CharField(unique=True)
    nif  = CharField(unique=True)
    logo = CharField(unique=True)
    taxt = DecimalField(decimal_places=2, max_digits=16)
    descricao = TextField(null=True)


def init_modes():
    db.connect()
    with db:
        db.create_tables(
            [
                Usuarios, Categorias, 
                Produtos, Fornecedor, 
                Estoque, Cliente,
                Pedidos, ItenPedido,
                Caixa, Vendas,
                Settings
            ]
        )
    
    try: 
        Usuarios.create(
            nome="Ricardo Cayoca",
            email="ricardokayoca@gmail.com",
            senha=generate_password_hash("admin"),
            user_type="admin"
        )
    except:
        ...





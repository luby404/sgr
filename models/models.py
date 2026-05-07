import uuid
from .db import orm, Model
from datetime import datetime, timedelta
from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash

class Empresa(Model):
    nome  = orm.CharField(unique=True)
    email = orm.CharField(unique=True)
    nif   = orm.CharField(unique=True)
    telefone    = orm.CharField(null=True)
   
    is_ative    = orm.BooleanField(default=True)

class Usuario(Model, UserMixin):
    
    class roles:
        admin   = "admin" # admin do sistema
        gestor  = "gestor"
        balcao  = "caixa"
    
    nome  = orm.CharField(max_length=256)
    email = orm.CharField(unique=True, max_length=256)
    senha = orm.CharField(max_length=256)
        
    user_type = orm.CharField(choices=[(i, i) for i in [roles.admin, roles.gestor, roles.balcao]])
    
    def check_password(self, senha:str):
        return check_password_hash(self.senha, senha)
    
    def set_password(self, senha:str):
        self.senha = generate_password_hash(senha)
        return self.senha

    def __str__(self):
        return self.nome
    

class Categoria(Model):
    nome            = orm.CharField()
    is_ative        = orm.BooleanField(default=True)
    cardapio        = orm.BooleanField(default=True)
    def __str__(self):
        return self.nome
    
class Produto(Model):
    
    categoria:Categoria = orm.ForeignKeyField(Categoria, backref="produtos")
    
    nome            = orm.CharField()
    capa            = orm.CharField()
    descricao       = orm.TextField()
    price           = orm.DecimalField(decimal_places=2, max_digits=16)
    is_ative        = orm.BooleanField(default=True)
    estoque         = orm.IntegerField(default=0)    
    
    cardapio        = orm.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nome} -> {self.estoque}"

class Estoque(Model):
    usuario    = orm.ForeignKeyField(Usuario, backref="estoque", null=True)
    produto    = orm.ForeignKeyField(Produto, backref="movimentacao")
    quantidade = orm.IntegerField(default=0)
    tipo       = orm.CharField(choices=[
        ("entrada", "entrada"),
        ("saida", "saida"),
        ("ajuste", "ajuste"),
    ]) 
    descricao = orm.TextField(null=True)
     
class Mesa(Model):
    nome            = orm.CharField()
    uuid            = orm.UUIDField(default=uuid.uuid4)
    status:bool     = orm.BooleanField(default=True) # true="aberto" false="fechado"
    
class Pedido(Model):
    
    class Status:
        pendente   = "pendente"
        preparacao = "em preparação"
        entregue   = "entregue"
        finalizado = "finalizado"
        cancelado  = "cancelado"
    
    mesa       = orm.ForeignKeyField(Mesa, backref="pedidos", null=True)
    aberto_em  = orm.DateTimeField(default=datetime.now)
    fechado_em = orm.DateTimeField(default=datetime.now)  
    
    usuario    = orm.ForeignKeyField(Usuario, backref="pedidos", null=True)
    total      = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    status     = orm.CharField(default=Status.pendente, choices=[
        (i, i) for i in [Status.pendente, Status.preparacao, Status.entregue, Status.finalizado, Status.cancelado]
    ])
    

class ItenPedido(Model):
    
    pubid   = orm.UUIDField(default=uuid.uuid4)
    
    pedido  = orm.ForeignKeyField(Pedido, backref="produtos")
    produto = orm.ForeignKeyField(Produto, backref="produtos")
    
    produto_nome  = orm.CharField(null=True)
    produto_price = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    quantidate = orm.IntegerField()
    subtotal   = orm.DecimalField(max_digits=16, decimal_places=2, default=0)





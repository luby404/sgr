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
        gestor  = "empresa_gestor"
        balcao  = "empresa_balcao"
        empresa = "empresa_admin"
    
    nome  = orm.CharField(max_length=256)
    email = orm.CharField(unique=True, max_length=256)
    senha = orm.CharField(max_length=256)
        
    user_type = orm.CharField(choices=[(i, i) for i in [roles.admin, roles.gestor, roles.balcao, roles.empresa]])
    empresa   = orm.ForeignKeyField(Empresa, backref="usuarios", null=True) 
    
    def check_password(self, senha:str):
        return check_password_hash(self.senha, senha)
    
    def set_password(self, senha:str):
        self.senha = generate_password_hash(senha)
        return self.senha
    

class Categoria(Model):
    nome            = orm.CharField()
    is_ative        = orm.BooleanField(default=True)
    empresa:Empresa = orm.ForeignKeyField(Empresa, backref="produtos")
    
    cardapio        = orm.BooleanField(default=True)
    
    
    def __str__(self):
        return self.nome
    

class Produto(Model):
    
    
    
    empresa:Empresa     = orm.ForeignKeyField(Empresa, backref="produtos")
    categoria:Categoria = orm.ForeignKeyField(Categoria, backref="produtos")
    
    nome            = orm.CharField()
    capa            = orm.CharField()
    descricao       = orm.TextField()
    price           = orm.DecimalField(decimal_places=2, max_digits=16)
    is_ative        = orm.BooleanField(default=True)
    estoque         = orm.IntegerField(default=0)    
    
    cardapio        = orm.BooleanField(default=True)

class Mesa(Model):
    empresa:Empresa = orm.ForeignKeyField(Empresa, backref="mesas")
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
    
    empresa = orm.ForeignKeyField(Empresa, backref="pedidos")
    mesa    = orm.ForeignKeyField(Mesa, backref="pedidos")
    
    aberto_em  = orm.DateTimeField(default=datetime.now)
    fechado_em = orm.DateTimeField(default=datetime.now)  
    
    total      = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    status     = orm.CharField(default=Status.pendente, choices=[
        (i, i) for i in [Status.pendente, Status.preparacao, Status.entregue, Status.finalizado, Status.cancelado]
    ])

class ItenPedido(Model):
    
    pubid   = orm.UUIDField(default=uuid.uuid4)
    
    empresa = orm.ForeignKeyField(Empresa, backref="pedidos")
    pedido  = orm.ForeignKeyField(Pedido, backref="produtos")
    produto = orm.ForeignKeyField(Produto, backref="produtos")
    
    produto_nome  = orm.CharField(null=True)
    produto_price = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    quantidate = orm.IntegerField()
    subtotal   = orm.DecimalField(max_digits=16, decimal_places=2, default=0)



class Plano(Model):
    nome  = orm.CharField()
    price = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    dias  = orm.IntegerField()


class Assinatura(Model):
    empresa         = orm.ForeignKeyField(Empresa, backref="assinaturas")
    plano           = orm.ForeignKeyField(Plano, backref="assinaturas")
    data_expiracao  = orm.DateTimeField()
    is_ative        = orm.BooleanField(default=True)

class Pagamento(Model):
    
    class Status:
        pago      = "pago"
        pendente  = "pendente"
        cancelado = "cancelado"
        
    
    assinatura = orm.ForeignKeyField(Assinatura, backref="pagamentos")
    status     = orm.CharField(
        choices=[
            (i, i)
            for i in [Status.pago, Status.pendente, Status.cancelado]
        ]
    )
    
    valor      = orm.DecimalField(max_digits=16, decimal_places=2, default=0)
    entidade   = orm.CharField()
    referencia = orm.CharField(unique=True)
    
    expira_em = orm.DateTimeField(default=lambda: datetime.now() + timedelta(minutes=15))
    
    



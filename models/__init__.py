from .db import db
from .models import (
    Usuario,
    Empresa,
    Produto,
    Comanda,
    Pedido,
    ItenPedido,
    Pagamento,
    Assinatura,
    Plano,
    Categoria
    
)


def init_db():
    db.connect()
    db.create_tables([
         Usuario,
        Empresa,
        Produto,
        Comanda,
        Pedido,
        ItenPedido,
        Pagamento,
        Assinatura,
        Plano,
        Categoria
    ])








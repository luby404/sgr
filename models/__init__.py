from .db import db
from .models import (
    Usuario,
    Empresa,
    Produto,
    Mesa,
    Pedido,
    ItenPedido,
    Categoria,
    Estoque,
    generate_password_hash
    
)


def init_db():
    db.connect()
    db.create_tables([
         Usuario,
        Empresa,
        Produto,
        Mesa,
        Pedido,
        ItenPedido,
        Categoria,
        Estoque
    ])
    try: 
        Usuario.create(
            nome="Ricardo Cayoca",
            email="ricardokayoca@gmail.com",
            senha=generate_password_hash("admin"),
            user_type=Usuario.roles.admin
        )
    except:
        pass







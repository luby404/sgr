from .base import Model

class PedidoAdmin(Model):
    column_list = ["mesa", "aberto_em", "fechado_em", "total"]
    roles       = ["empresa_gestor", "empresa_admin"]
    
    can_create = False
    


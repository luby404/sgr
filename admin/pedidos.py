from .base import Model

from models  import Mesa, Pedido

class PedidoAdmin(Model):
    column_list = ["mesa", "aberto_em", "fechado_em", "total", "status"]
    roles       = ["empresa_gestor", "empresa_admin"]
    can_create = False
    
    def on_model_change(self, form, model:Pedido, is_created):
        
        if not is_created:
            mesa:Mesa = Mesa.get_or_none(Mesa.id == model.mesa.id)
            if mesa:
                if model.status in [Pedido.Status.cancelado, Pedido.Status.finalizado]:
                    mesa.status = True
                else:
                    mesa.status = False
                mesa.save()
        
        return super().on_model_change(form, model, is_created)
    


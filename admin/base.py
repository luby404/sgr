from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib.peewee import ModelView


from models import Usuario

class Model(ModelView):
    
    roles = ["admin"]
        
    edit_modal   = True
    create_modal = True
    details_modal = True
    
    can_view_details = True
    
    user:Usuario = None
    
    form_excluded_columns = ["criado_em", "atualizado_em", "is_ative", "empresa", "cardapio"]
    
    """def get_query(self):
        return super().get_query().where(
            self.model.empresa == current_user.empresa
        )

    def get_count_query(self):
        return super().get_count_query().where(
            self.model.empresa == current_user.empresa
        )"""
    
    
    def set_roles(self):
        ...
    
    def is_accessible(self):
                
        view = False
        self.user:Usuario = current_user
        if self.user.is_authenticated and self.user.user_type in self.roles:
            view = True
            self.set_roles()
        
        
        return view

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))
    
    def get_query(self):

        query = super().get_query()
        
        try:
            query = query.where(
                self.model.empresa == current_user.empresa
            )
        except:
            ...
            
        return query
    
        
    
    def get_count_query(self):

        query = super().get_count_query()
        query = query.where(
            self.model.empresa == current_user.empresa
        )

        return query
    
    
    
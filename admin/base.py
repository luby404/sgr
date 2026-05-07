from flask import redirect, url_for
from flask_login import current_user
from flask_admin.contrib.peewee import ModelView

from flask_admin.menu import MenuLink, MenuDivider

from models import Usuario

class Model(ModelView):
    
    roles = ["admin"]
        
    edit_modal   = True
    create_modal = True
    details_modal = True
    
    can_view_details = True
    
    user:Usuario = None
    
    form_excluded_columns = ["criado_em", "atualizado_em", "is_ative", "empresa", "cardapio", "usuario"]
 
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
    
    
    

class Link(MenuLink):
    
    roles = ["admin", "gestor", "caixa"]
    user = None
    
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



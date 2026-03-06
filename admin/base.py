from flask_admin.contrib.peewee import ModelView


class Model(ModelView):
    edit_modal   = True
    create_modal = True
    
    form_excluded_columns = ["criado_em", "atualizado_em"]
    
    
    
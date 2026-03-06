import peewee as orm
from datetime import datetime


db = orm.SqliteDatabase("banco.db")

class Model(orm.Model):
    
    criado_em     = orm.DateTimeField(default=datetime.now)
    atualizado_em = orm.DateTimeField(default=datetime.now)
    
    def save(self, *a, **k):
        self.atualizado_em = datetime.now()
        return super().save(*a, **k)
    
    
    class Meta:
        database = db
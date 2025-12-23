from peewee import (
    Model,
    SqliteDatabase,
    PostgresqlDatabase,

    DateTimeField,
    BooleanField,
)

from datetime import datetime

db = SqliteDatabase("banco.db")

class BaseModel(Model):
    is_ative  = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.now)
    atualizado_em = DateTimeField(default=datetime.now)

    def save(self, *a, **b):

        self.atualizado_em = datetime.now()

        return super().save(*a, **b)

    class Meta:
        database = db

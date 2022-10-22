from peewee import Model
from load import database
# database = SqliteDatabase("users.db")  # todo: fix

class BaseModel(Model):
    class Meta:
        database = database

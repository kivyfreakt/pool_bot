from peewee import PrimaryKeyField, CharField
from models.base import BaseModel


class Users(BaseModel):
    user_id = PrimaryKeyField(null=False)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    username = CharField(max_length=128)

    class Meta:
        db_table = "users"

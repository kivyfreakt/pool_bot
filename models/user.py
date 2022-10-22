""" Модуль для класса пользователей """

from peewee import PrimaryKeyField, CharField
from models.base import BaseModel


class Users(BaseModel):
    """ Модель пользователей """
    user_id = PrimaryKeyField(null=False)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    username = CharField(max_length=128)

    class Meta:
        """ Класс для конфигурции модели """
        db_table = "users"

""" Модуль для базового класса """

from peewee import Model
from load import database


class BaseModel(Model):
    """ Базовая модель для наследования """
    class Meta:
        """ Класс для конфигурции модели """
        database = database

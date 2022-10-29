""" Модуль для класса ответов """

import json
from peewee import PrimaryKeyField, IntegerField, BooleanField, ForeignKeyField, TextField
from models.base import BaseModel
from models.user import Users


class JSONField(TextField):
    """ Класс фейкового JSON поля """
    field_type = 'json'

    def db_value(self, value):
        """Convert the python value for storage in the database."""
        return value if value is None else json.dumps(value, ensure_ascii=False)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        return value if value is None else json.loads(value)


class Responses(BaseModel):
    """ Модель ответа """
    resp_id = PrimaryKeyField(null=False)
    step = IntegerField(default=0)
    completed = BooleanField(default=False)
    details = JSONField()
    user = ForeignKeyField(Users, related_name='responses',
                           to_field='user_id', on_delete='cascade', on_update='cascade')

    class Meta:
        """ Класс для конфигурции модели """
        db_table = "responses"

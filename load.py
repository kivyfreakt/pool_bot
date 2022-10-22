""" Файл для создания базы данных """
from peewee import SqliteDatabase

database = SqliteDatabase("users.db")

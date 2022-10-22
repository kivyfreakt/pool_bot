from peewee import PrimaryKeyField, IntegerField, BooleanField, ForeignKeyField, TextField
from models.base import BaseModel
from models.user import Users
import json

# class Response(models.Model):

#     step = models.SmallIntegerField(default=0)
#     details = jsonfield.JSONField(max_length=8192, default=dict)
#     respondent = models.ForeignKey(Respondent, related_name="responses", on_delete=models.CASCADE)

#     completed = models.BooleanField(default=False)

#     @property
#     def html(self):
#         table = "<table class='table'>"

#         for question in self.details:
#             answer = self.details[question]
#             table += f"""
#                 <tr>
#                     <td>{question}</td>
#                     <td><b>{answer}</b></td>
#                 </tr>
#             """

#         table += "</table>"
#         return format_html(table)

class JSONField(TextField):
    field_type = 'json'
    """
    Class to "fake" a JSON field with a text field. Not efficient but works nicely
    """
    def db_value(self, value):
        """Convert the python value for storage in the database."""
        return value if value is None else json.dumps(value)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        return value if value is None else json.loads(value)

class Responses(BaseModel):
    resp_id = PrimaryKeyField(null = False)
    step = IntegerField(default = 0)
    completed = BooleanField(default = False)
    details = JSONField()
    user = ForeignKeyField(Users, related_name='responses',
                           to_field='user_id', on_delete='cascade', on_update='cascade')

    class Meta:
        db_table = "responses"

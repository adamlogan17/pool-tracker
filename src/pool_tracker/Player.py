from mongoengine import Document, StringField, IntField, BooleanField

class Player(Document):
    _minimum_elo = 100
    name = StringField(required=True, unique=True)
    elo = IntField(required=True, min_value=_minimum_elo, default = 400)
    active = BooleanField(required=True, default=True)

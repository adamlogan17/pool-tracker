from mongoengine import Document, StringField, IntField, BooleanField
import json

class Player(Document):
    _minimum_elo = 100
    name = StringField(required=True, unique=True)
    elo = IntField(required=True, min_value=_minimum_elo, default = 400)
    active = BooleanField(required=True, default=True)
    
    def to_dict(self):
        json_str = self.to_json()
        player_dict = json.loads(json_str)
        player_dict['id'] = player_dict['_id']['$oid']
        del player_dict['_id']
        return player_dict

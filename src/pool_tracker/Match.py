from datetime import datetime, timezone
import json
from mongoengine import Document, IntField, ReferenceField, DateTimeField, signals
from pool_tracker.elo import update_elo
from pool_tracker.Player import Player

class SamePlayerMatchException(Exception):
    message = "A player cannot play themselves."

    def __init__(self):
        super().__init__(self.message)

    def __str__(self):
        return f"Error: {self.message}"

class Match(Document):
    winning_player = ReferenceField(Player, required=True)
    losing_player = ReferenceField(Player, required=True)
    match_time = DateTimeField(required=True, default=datetime.now(timezone.utc))
    winning_player_elo_before = IntField(required=True)
    losing_player_elo_before = IntField(required=True)
    winning_player_elo_after = IntField(required=True)
    losing_player_elo_after = IntField(required=True)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if document.winning_player == document.losing_player:
            # TODO: Make this a custom error
            raise SamePlayerMatchException
        document.winning_player_elo_before = document.winning_player.elo
        document.losing_player_elo_before = document.losing_player.elo
        update_elo(document.winning_player, document.losing_player)
        document.winning_player_elo_after = document.winning_player.elo
        document.losing_player_elo_after = document.losing_player.elo

    def to_dict(self):
        json_str = self.to_json()
        match_dict = json.loads(json_str)
        match_dict['id'] = match_dict['_id']['$oid']
        del match_dict['_id']
        match_dict['match_time'] = match_dict['match_time']['$date']
        match_dict['winning_player'] = Player.objects(id=match_dict['winning_player']['$oid']).first().to_dict()
        match_dict['losing_player'] = Player.objects(id=match_dict['losing_player']['$oid']).first().to_dict()
        return match_dict

signals.pre_save.connect(Match.pre_save, sender=Match)
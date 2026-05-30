from datetime import datetime, timezone

from mongoengine import Document, IntField, ReferenceField, DateTimeField, signals
from pool_tracker.elo import update_elo
from pool_tracker.Player import Player



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
        document.winning_player_elo_before = document.winning_player.elo
        document.losing_player_elo_before = document.losing_player.elo
        update_elo(document.winning_player, document.losing_player)
        document.winning_player_elo_after = document.winning_player.elo
        document.losing_player_elo_after = document.losing_player.elo

signals.pre_save.connect(Match.pre_save, sender=Match)
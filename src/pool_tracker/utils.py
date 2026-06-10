from mongoengine import connect
import os
from pool_tracker.Player import Player
from pool_tracker.Match import Match

def connect_db(db_name=os.getenv('APP_DB', 'eloTracker'), host=f"mongodb://{os.getenv('MONGO_DB', 'leaderboard')}"):
    # TODO: Maybe move the connection code into __init__.py (maybe have an env var that checks if a mongo_db is given)?
    connect(host=host, username="user", password="pass", authentication_source='admin', db=db_name)

def get_all_players():
    players = Player.objects
    all_players = [player.to_dict() for player in players]
    return all_players

def inactivate_player(name):
    player = Player.objects(name=name).first()
    player.active = False
    player.save()
    return player

def get_player_info(name):
    player = Player.objects(name=name, active=True).first()
    if not player:
        return None
    won_matches = Match.objects(winning_player=player)
    lost_matches = Match.objects(losing_player=player)
    
    return {
        **player.to_dict(),
        'won_matches': [match.to_dict() for match in won_matches],
        'lost_matches': [match.to_dict() for match in lost_matches]
    }

def get_match_by_players(player1, player2):
    player1_obj = Player.objects(name=player1).first()
    player2_obj = Player.objects(name=player2).first()
    player1_win = Match.objects(winning_player=player1_obj, losing_player=player2_obj)
    player2_win = Match.objects(winning_player=player2_obj, losing_player=player1_obj)
    matches = [match.to_dict() for match in player1_win] + [match.to_dict() for match in player2_win]
    return matches

def get_all_matches():
    matches = Match.objects.order_by('match_time')
    all_matches = [match.to_dict() for match in matches]
    return all_matches

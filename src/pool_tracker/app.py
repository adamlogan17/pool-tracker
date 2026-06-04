from flask import Flask, jsonify, request
from mongoengine import connect
import os
from pool_tracker.Player import Player
from pool_tracker.Match import Match
from mongoengine.errors import NotUniqueError

app = Flask(__name__)

host = f"mongodb://{os.getenv('MONGO_DB', 'leaderboard')}"
connect(host=host, username="user", password="pass", authentication_source='admin')

@app.route('/player/<string:name>', methods=['GET'])
def get_player(name):
    player = Player.objects(name=name).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(player.to_dict()), 200

@app.route('/player/all', methods=['GET'])
def get_all_players():
    players = Player.objects
    all_players = [player.to_dict() for player in players]
    return jsonify({
        'players': all_players
    }), 200

@app.route('/player', methods=['POST'])
def create_player():
    request_body = request.json
    if 'name' not in request_body:
        return jsonify({
            "error": "Must provide player name."
        }), 400
    try:
        new_player = Player(name=request_body['name']).save()
    except NotUniqueError:
        return jsonify({
            "error": "User already exists"
        }), 400
    return jsonify(new_player.to_dict()), 200

@app.route('/player/<string:name>', methods=['DELETE'])
def inactivate_player(name):
    player = Player.objects(name=name).first()
    if not player:
        return jsonify({
            "error": "Player does not exist"
        }), 400
    player.active = False
    player.save()
    return jsonify(player.to_dict()), 200

@app.route('/match/<string:player1>/<string:player2>', methods=['GET'])
def get_match_by_players(player1, player2):
    player1_obj = Player.objects(name=player1).first()
    player2_obj = Player.objects(name=player2).first()
    player1_win = Match.objects(winning_player=player1_obj, losing_player=player2_obj)
    player2_win = Match.objects(winning_player=player2_obj, losing_player=player1_obj)
    matches = [match.to_dict() for match in player1_win] +[match.to_dict() for match in player2_win]
    return jsonify({
        'matches': matches
    }), 200

@app.route('/match/all', methods=['GET'])
def get_all_matches():
    matches = Match.objects.order_by('match_time')
    all_matches = [match.to_dict() for match in matches]
    return jsonify({
        'matches': all_matches
    }), 200

@app.route('/match', methods=['POST'])
def create_match():
    request_body = request.json
    if "winner" not in request_body or "loser" not in request_body:
        return jsonify({
            "error": "Must provide 'winner' and 'loser'"
        }), 400
    winning_player = Player.objects(name=request_body['winner'], active=True).first()
    if not winning_player:
        return jsonify({
            "error": "Winning player does not exist."
        }), 400
    losing_player = Player.objects(name=request_body['loser'], active=True).first()
    if not losing_player:
        return jsonify({
            "error": "Losing player does not exist"
        }), 400
    if winning_player == losing_player:
        return jsonify({
            "error": "Cannot have a match of the same player"
        }), 400
    match = Match(winning_player=winning_player, losing_player=losing_player).save()
    return jsonify(match.to_dict()), 200

def launch_server():
    DEBUG = os.getenv("DEBUG", False) == "true"
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)

if __name__ == '__main__':
    launch_server()
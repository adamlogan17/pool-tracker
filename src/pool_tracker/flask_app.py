from flask import Flask, jsonify, request
import os
from pool_tracker.Player import Player
from pool_tracker.Match import Match, SamePlayerMatchException
from mongoengine.errors import NotUniqueError
from pool_tracker.utils import connect_db, get_all_players, inactivate_player, get_match_by_players, get_all_matches

app = Flask(__name__)

connect_db()

@app.route('/player/<string:name>', methods=['GET'])
def get_player(name):
    player = Player.objects(name=name).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(player.to_dict()), 200

@app.route('/player/all', methods=['GET'])
def request_get_all_players():
    return jsonify({
        'players': get_all_players()
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
def request_inactivate_player(name):
    try:
        player = inactivate_player(name)
    except Exception as e:
        return jsonify({
            'error': 'player not found'
        }), 404
    return jsonify(player.to_dict()), 200

@app.route('/match/<string:player1>/<string:player2>', methods=['GET'])
def request_get_match_by_players(player1, player2):
    return jsonify({
        'matches': get_match_by_players(player1, player2)
    }), 200

@app.route('/match/all', methods=['GET'])
def request_get_all_matches():
    return jsonify({
        'matches': get_all_matches()
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
    match = None
    try:
        match = Match(winning_player=winning_player, losing_player=losing_player).save()
    except SamePlayerMatchException as e:
        return jsonify({
            'error': str(e)
        }), 500
    return jsonify(match.to_dict()), 200

def launch_server():
    DEBUG = os.getenv("DEBUG", False) == "true"
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)

if __name__ == '__main__':
    launch_server()
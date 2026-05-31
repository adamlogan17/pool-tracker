from flask import Flask, jsonify
from mongoengine import connect
import os
from pool_tracker.Player import Player

app = Flask(__name__)

host = f"mongodb://{os.getenv('MONGO_DB', 'leaderboard')}"
connect(host=host, username="user", password="pass", authentication_source='admin')

@app.route('/player/<string:name>', methods=['GET'])
def get_player(name):
    player = Player.objects(name=name).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify({
        'name': player.name
    })

@app.route('/player/all', methods=['GET'])
def get_all_players():
    return 'Hello World'

@app.route('/player', methods=['POST'])
def create_player():
    return 'Hello World'

@app.route('/player', methods=['DELETE'])
def inactivate_player():
    return 'Hello World'

@app.route('/match/<string:winner>/<string:loser>', methods=['GET'])
def get_match_by_players(winner, loser):
    return 'Hello World'

@app.route('/match/all', methods=['GET'])
def get_all_matches():
    # Get all matches, with most recent first
    return 'Hello World'

@app.route('/match', methods=['POST'])
def create_match():
    return 'Hello World'

def launch_server():
    DEBUG = os.getenv("DEBUG", False) == "true"
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)

if __name__ == '__main__':
    launch_server()
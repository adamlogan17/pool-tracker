from flask import Flask
from mongoengine import connect
import os

app = Flask(__name__)

host = f"mongodb://{os.getenv('MONGO_DB', 'leaderboard')}"
connect(host=host, username="user", password="pass", authentication_source='admin')

@app.route('/player/<string:name>', methods=['GET'])
def get_player(name):
    return "Hello World"

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
    app.run()

if __name__ == '__main__':
    launch_server()
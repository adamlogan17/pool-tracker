from mongoengine import connect
import os
from faker import Faker

from pool_tracker.Player import Player
from pool_tracker.Match import Match


def main() -> None:
    db_name = os.getenv('APP_DB', 'eloTracker')
    host = f"mongodb://{os.getenv('MONGO_DB', 'leaderboard')}"
    connect(host=host, username="user", password="pass", authentication_source='admin', db=db_name)

    print("Hello from pool-tracker!")
    fake = Faker('en_GB')
    name = fake.first_name()
    print(f"Create player: {name}")
    player2 = Player(name=name).save()
    print(player2.name)

    player1 = Player.objects(name="Adam").first()
    print(player1.name)

    match = Match(winning_player=player1, losing_player=player2).save()
    
    print('winning player:', match.winning_player.name)
    print('current elo:', player1.elo)
    print('prev elo:', match.winning_player_elo_before)
    print('win elo:', match.winning_player_elo_after)
    print('\n', '-'*40, '\n')
    print('losing player', match.losing_player.name)
    print('current elo:', player2.elo)
    print('prev elo:', match.losing_player_elo_before)
    print('win elo:', match.losing_player_elo_after)
    print('')


if __name__ == "__main__":
    main()

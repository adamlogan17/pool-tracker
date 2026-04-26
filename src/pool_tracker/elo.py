class Player():
    _minimum_elo = 100

    def __init__(self, name: str):
        self.name = name
        self.elo = 400

    @property
    def name(self) -> str: return self._name

    @name.setter
    def name(self, name: str): self._name = name

    @property
    def elo(self) -> int: return self._elo

    @elo.setter
    def elo(self, elo: int):
        if elo < self._minimum_elo:
            print(f"Invalid, elo must be greater than {self._minimum_elo}")
        else:
            self._elo = elo

def elo_formula(rating: int, win: bool, prob_of_winning: float) -> int:
    K = 32
    return round(rating + (K * (int(win) - prob_of_winning)))

def probability_of_winning(winning_rating: int, losing_rating: int) -> float:
    s = 400
    return 1 / (1 + 10**((losing_rating - winning_rating) / s))

# This is in a win/loss game. There is no draw
def update_elo(winning_player: Player, losing_player: Player):
    # Probability of winning player winning
    prob_of_win = probability_of_winning(winning_player.elo, losing_player.elo)

    # Probability of losing player winning
    # As this is a win loss game, this works, otherwise the formula `1 / (1 + 10**((winning_player.elo - losing_player.elo) / s))`, should be used
    prob_of_lose = 1 - prob_of_win

    # update elo rating
    # example: player.elo = round(player.elo + (K * (win_as_bool - prob_of_win)))
    winning_player.elo = elo_formula(winning_player.elo, True, prob_of_win)
    losing_player.elo = elo_formula(losing_player.elo, False, prob_of_lose)




if __name__ == "__main__":
    x = Player("Adam")
    y = Player("Dean")

    update_elo(x, y)

    print(x.elo)
    print(y.elo)

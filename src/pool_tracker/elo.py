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

if __name__ == "__main__":
    x = Player("Adam")
    y = Player("Dean")




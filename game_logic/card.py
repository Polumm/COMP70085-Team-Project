class Card:
    def __init__(self, secret_index: int) -> None:
        self._revealed: bool = False
        self._secret_index: int = secret_index

    def flip(self) -> None:
        self._revealed = not self._revealed

    def is_revealed(self) -> bool:
        return self._revealed

    def get_secret_index(self) -> int:
        return self._secret_index

    def set_revealed(self, revealed: bool) -> None:
        self._revealed = revealed

    def __str__(self) -> str:
        return f"Card(revealed={self._revealed}, secret={self._secret_index})"

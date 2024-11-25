import unittest

from game_logic.game_state import Game
from game_logic.card import Card


class TestGame(unittest.TestCase):
    def test_game(self):
        test_cards = [
            Card(0),
            Card(4),
            Card(4),
            Card(2),
            Card(0),
            Card(1),
            Card(3),
            Card(2),
            Card(0),
            Card(3),
        ]
        test_game = Game(board_size=10, test_cards=test_cards)
        test_game.flip(0)
        test_game.flip(1)
        test_game.flip(2)
        test_game.flip(3)
        test_game.flip(4)
        test_game.flip(5)
        test_game.flip(0)
        test_game.flip(4)
        answer_board = [
            None,
            Card(4),
            Card(4),
            Card(2),
            None,
            Card(1),
            Card(3),
            Card(2),
            Card(0),
            Card(3),
        ]
        answer_game = Game(10)
        answer_game.set_board(answer_board)
        assert str(test_game) == str(answer_game)

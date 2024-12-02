from collections.abc import MutableSequence
from typing import Optional
from random import shuffle
import json
from time import time

from game_logic.card import Card
from game_logic.json_encoder import GameEncoder


class Game:
    def __init__(
        self, num_pairs: int, test_cards: Optional[list[Card]] = None
    ) -> None:
        self._num_pairs: int = num_pairs

        if test_cards is None:
            self._cards: MutableSequence[Optional[Card]] = list(
                [Card(secret_index=i) for i in range(num_pairs)]
                + [Card(secret_index=i) for i in range(num_pairs)]
            )  # add a list() to pass type check

            shuffle(self._cards)  # make the order of the cards random
        else:
            assert num_pairs * 2 == len(
                test_cards
            ), "The board size doesn't match the board you gave me!"
            self._cards = list(test_cards)

        self._revealed_card_index: Optional[int] = None

        self._time: float = 0.0
        self._flip_count: int = 0

    def flip(self, target: int) -> int:
        if self._time == 0:
            self._time = time()

        self._flip_count += 1

        target_card = self._cards[target]

        # you can't flip a non-existent card
        if target_card is None:
            return -1

        # you can't flip a revealed card
        if target_card.is_revealed():
            return -1

        if self._revealed_card_index is not None:
            # currently there is a revealed card
            if not self._compare_index(target):
                # if the revealed card doesn't match the card being flipped
                revealed_card = self._get_revealed_card()

                # flip the revealed card back
                revealed_card.flip()
                self._has_revealed_card = False
                self._revealed_card_index = None
            else:
                # they do match
                assert self._revealed_card_index is not None, "Buggy state"

                # remove both cards
                self._remove_card(self._revealed_card_index)
                self._remove_card(target)

            return target_card.get_secret_index()
        else:
            # a normal flip
            self._has_revealed_card = True
            self._revealed_card_index = target
            target_card.flip()

            return target_card.get_secret_index()

    def __str__(self) -> str:
        return str([str(card) for card in self._cards])

    def get_json_str(self) -> str:
        return json.dumps(self, indent=4, cls=GameEncoder)

    def get_time(self) -> float:
        return 0.0 if self._time == 0.0 else time() - self._time

    def get_flip_count(self) -> int:
        return self._flip_count

    def get_num_pairs(self) -> int:
        return self._num_pairs

    def detect_finished(self) -> bool:
        return all(card is None for card in self._cards)

    # This method is only for testing purposes
    def force_reveal(self, target: int):
        target_card = self._get_card(target)
        target_card.set_revealed(True)

    # This method is only for testing purposes
    def clear_card(self, target: int):
        self._cards[target] = None

    # This method is only for testing purposes
    def set_board(self, board: MutableSequence[Optional[Card]]):
        self._cards = board

    def _get_card(self, target: int) -> Card:
        target_card = self._cards[target]
        assert target_card is not None, "Buggy state"
        return target_card

    def _compare_index(self, target: int):
        assert self._revealed_card_index is not None, "Buggy state"
        target_card = self._cards[target]
        assert target_card is not None, "Buggy state"
        revealed_card = self._cards[self._revealed_card_index]
        assert revealed_card is not None, "Buggy state"

        return (
            target_card.get_secret_index() == revealed_card.get_secret_index()
        )

    def _remove_card(self, target: int):
        self._cards[target] = None
        if target == self._revealed_card_index:
            self._revealed_card_index = None

    def _get_revealed_card(self) -> Card:
        assert self._revealed_card_index is not None, "Buggy state"
        revealed_card = self._cards[self._revealed_card_index]
        assert revealed_card is not None, "Buggy state"
        return revealed_card


games: dict[int, Game] = {}

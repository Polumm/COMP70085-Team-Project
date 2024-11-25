from collections.abc import MutableSequence
from typing import Optional
from game_logic.card import Card
from random import shuffle


class Game:
    def __init__(
        self, board_size: int, test_cards: Optional[list[Card]] = None
    ) -> None:
        self._board_size: int = board_size
        assert board_size % 2 == 0, "The board size must be an even number!"

        if test_cards is None:
            self._cards: MutableSequence[Optional[Card]] = list(
                [Card(secret_index=i) for i in range(board_size // 2)]
                + [Card(secret_index=i) for i in range(board_size // 2)]
            )  # add a list() to pass type check

            shuffle(self._cards)  # make the order of the cards random
        else:
            assert board_size == len(
                test_cards
            ), "The board size doesn't match the board you gave me!"
            self._cards = list(test_cards)

        self._revealed_card_index: Optional[int] = None

    def flip(self, target: int) -> Optional[int]:
        target_card = self._cards[target]

        if target_card is None:
            return

        if target_card.is_revealed():
            return

        if self._revealed_card_index is not None:
            if not self._compare_index(target):
                self._has_revealed_card = False
                revealed_card = self._get_revealed_card()
                revealed_card.flip()
                self._revealed_card_index = None
                return target_card.get_secret_index()
            else:
                assert self._revealed_card_index is not None, "Buggy state"
                self._remove_card(self._revealed_card_index)
                self._remove_card(target)
                return
        else:
            self._has_revealed_card = True
            self._revealed_card_index = target
            target_card.flip()
            return

    def __str__(self) -> str:
        return str([str(card) for card in self._cards])

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

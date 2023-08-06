"""Create class for representing and printing a playing card"""
# See terminal_playing_cards/view.py for why these are disabled
# pylint: disable=missing-docstring
# pylint: disable=bad-continuation
from functools import total_ordering
from colorama import init
from terminal_playing_cards.utils import convert_layers_to_string
from terminal_playing_cards.config import (
    SUIT_SYMBOL_DICT,
    CARD_FACE_DICT,
    CARD_BACK_STYLE,
)

# Change the color back to default after each print
# Prevents user input from being colored
init(autoreset=True)


@total_ordering
class Card(object):
    """A playing card in a standard deck.

    Designed to look like a standard playing card when
    printed to the terminal. For example:

    from terminal_playing_cards import Card

    ace_spades = Card("A", "spades")
    print(ace_spades)

    A list of Card objects is the main attribute of the
    View and Deck classes.

    Attributes:
        face: Card face. For example: "A", "10", "Q".
            See terminal_playing_cards.config.CARD_FACE_DICT
            for valid options.
        suit: Card suit. For example: "spades", "hearts".
            See terminal_playing_cards.config.SUIT_SYMBOL_DICT
            for valid options.
        value: Integer value of the Card. Defaults to 0.
        kwargs: Card initialization options. See kwargs
            in help(Deck) for further information.
    """

    def __init__(self, face: str, suit: str, value: int = 0, **kwargs: bool):
        self._face = None
        self.face = face
        self._suit = None
        self.suit = suit
        self.value = value
        self.hidden = kwargs.get("hidden", False)
        self.picture = kwargs.get("picture", True)

    @property
    def face(self):
        return self._face

    @face.setter
    def face(self, value):
        value = value.upper()
        if value in CARD_FACE_DICT.keys():
            self._face = value
        else:
            raise NotImplementedError(f"'{value}' is not a valid face for a Card")

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        value = value.lower()
        if value in SUIT_SYMBOL_DICT.keys():
            self._suit = value
        else:
            raise NotImplementedError(f"'{value}' is not a valid suit for a Card")

    def _create_card_grid(self) -> list:
        """Creates a standard empty grid template for all playing cards."""
        card_grid = [[" " for _ in range(11)] for _ in range(7)]
        # Add extra space if the face is two characters instead of one
        if len(self.face) > 1 and not self.hidden:
            for layer in range(1, 6):
                card_grid[layer].append(" ")

        return card_grid

    def _populate_corners_and_center(self, card_grid: list) -> list:
        """
        Populates the corners of card grid with face and suit and
        the center with a picture for face cards.
        """
        symbol = SUIT_SYMBOL_DICT.get(self.suit).get("symbol")
        card_grid[0][0] = self.face
        card_grid[1][0] = symbol
        if self.picture:
            card_grid[3][5] = CARD_FACE_DICT.get(self.face).get("picture", " ")
        card_grid[5][10] = symbol
        card_grid[6][10] = self.face
        return card_grid

    def _populate_back_of_card(self, card_grid: list) -> list:
        """Populates the card grid with a design for the back of the card."""
        for layer in range(7):
            for position in [0, 1, 9, 10]:
                card_grid[layer][position] = "|"

        if self.picture:
            card_grid[2][5] = "🚲"
            card_grid[4][5] = "🚲"

        return card_grid

    def _plan_card_grid(self) -> list:
        """Fills out the card grid according to given symbol coordinates."""
        card_grid = self._create_card_grid()

        if self.hidden:
            return self._populate_back_of_card(card_grid)

        card_grid = self._populate_corners_and_center(card_grid)
        symbol_coords = CARD_FACE_DICT.get(self.face).get("coords")

        if not symbol_coords:
            return card_grid

        for layer, position in symbol_coords:
            card_grid[layer][position] = SUIT_SYMBOL_DICT.get(self.suit).get("symbol")

        return card_grid

    def _get_style(self) -> str:
        """Retrives the colorama codes for a card style."""
        return (
            SUIT_SYMBOL_DICT.get(self.suit).get("style")
            if not self.hidden
            else CARD_BACK_STYLE
        )

    def __str__(self):
        """Makes the card look like an actual playing card."""
        card_grid_plan = self._plan_card_grid()
        card_str = convert_layers_to_string(card_grid_plan)

        return self._get_style() + card_str

    def __repr__(self):
        return (
            f"Card('{self.face}', '{self.suit}', "
            f"value={self.value}, hidden={self.hidden}, picture={self.picture})"
        )

    def __getitem__(self, key):
        return self._plan_card_grid()[key]

    # All magic methods are designed to work for comparing cards against
    # other Card objects or numbers
    def __eq__(self, other):
        try:
            result = self.value == other.value
        except AttributeError:
            result = self.value == other
        return result

    def __lt__(self, other):
        try:
            result = self.value < other.value
        except AttributeError:
            result = self.value < other
        return result

    def __add__(self, other):
        try:
            result = self.value + other.value
        except AttributeError:
            result = self.value + other
        return result

    def __radd__(self, other):
        try:
            result = other.value + self.value
        except AttributeError:
            result = other + self.value
        return result

    def __sub__(self, other):
        try:
            result = self.value - other.value
        except AttributeError:
            result = self.value - other
        return result

    def __rsub__(self, other):
        try:
            result = other.value - self.value
        except AttributeError:
            result = other - self.value
        return result

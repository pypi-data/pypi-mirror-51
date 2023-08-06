"""Create class for a View of Card objects"""
# Disable this pylint rule because of a conflict with black
# See: github.com/python/black/issues/48
# pylint: disable=bad-continuation
# Ignore concerns about docstrings, since not _all_ methods need a docstring
# according to Google style guide
# pylint: disable=missing-docstring

from colorama import Style, Fore
from terminal_playing_cards.deck import Deck
from terminal_playing_cards.utils import convert_layers_to_string


class View(Deck):
    """A view one or more Cards.
    
    Inherits the methods, but not the attributes, from the Deck
    class. Designed to be printed in a terminal window alongside
    other Card objects. For example:

    from terminal_playing_cards import Card, View

    ace_spades = Card("A", "spades")
    ace_hearts = Card("A", "hearts")

    hand = View([ace_spades, ace_hearts])
    print(hand)
    # Overlap cards on each other
    hand = View([ace_spades, ace_hearts], spacing=-5)
    print(hand)
    
    Attributes:
        cards: A list of Cards.
        orientation: How to display the cards when printed
            to the terminal. Defaults to "horizontal".
        spacing: How far apart to space the cards when
            printed to the terminal. Negative spacing (placing
            a card on top of the previous card) is allowed.
            Defaults to 2.
    """

    # No need to initialize Deck when View is created. Only looking to inherit
    # methods, not attributes
    # pylint: disable=super-init-not-called
    def __init__(self, cards: list, orientation: str = "horizontal", spacing: int = 2):
        self.cards = cards
        self._orientation = None
        self.orientation = orientation
        self._spacing = None
        self.spacing = spacing

    # pylint: enable=super-init-not-called

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        if orientation in ["horizontal", "vertical"]:
            self._orientation = orientation
        else:
            raise NotImplementedError(
                f"The View class cannot place cards {orientation}ly"
            )

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, spacing):
        if spacing > -11:
            self._spacing = spacing
        else:
            raise NotImplementedError(
                "The View class cannot have spacing less than -10"
            )

    def _merge_horizontal(self) -> list:
        """Merges all cards in the View horizontally."""
        merged_grid = []
        positive_spacing = [" " for _ in range(self._spacing)]
        # Combine the cards in the View at the grid layer level
        for layer in range(7):
            merged_layer = []
            card_position = 0
            for card in self:
                # Need to know if the previous card was hidden or if it had a
                # long face (like "10" or "JK") in order to know how to handle
                # negative spacing when merging for the current layer
                prev_card = (
                    self[card_position - 1] if card_position != 0 else DummyCard()
                )
                # pylint: disable=protected-access
                card_style = [card._get_style()]
                # pylint: enable=protected-access
                card_layer = card_style + card[layer] + [Style.RESET_ALL]
                if self._spacing >= 0:
                    merged_layer += card_layer + positive_spacing
                else:
                    border = [Fore.BLACK, "|"] if card_position != 0 else []
                    prev_face_is_len_two = (
                        len(prev_card.face) == 2 and not prev_card.hidden
                    )
                    on_last_layer = layer == 6
                    negative_spacing = (
                        self._spacing
                        if not (prev_face_is_len_two)
                        or (prev_face_is_len_two and on_last_layer)
                        else self._spacing - 1
                    )
                    merged_layer = merged_layer[:negative_spacing] + border + card_layer
                    card_position += 1
            merged_grid.append(merged_layer)

        return merged_grid

    def _merge_vertical(self) -> list:
        """Merge all cards in the View vertically."""
        raise NotImplementedError(
            "Vertical orientation currently not implemented for the View class"
        )

    def __str__(self):
        """Makes the View look like a collection of playing cards."""
        merge_fx = getattr(self, f"_merge_{self._orientation}")
        # Merge playing cards in desired direction
        merged_cards = merge_fx()
        return convert_layers_to_string(merged_cards)


# Dummy object used by View to determine how to merge cards
# pylint: disable=too-few-public-methods
class DummyCard:
    def __init__(self):
        self.face = " "
        self.hidden = False


# pylint: enable=too-few-public-methods

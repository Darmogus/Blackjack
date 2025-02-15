# --- External libraries ---
from enum import Enum, IntEnum
from termcolor import colored


# --- Constants ---
class CardValues(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11  # Ace can be 1 or 11

class CardSuits(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


# --- Classes ---
class Card:
    SUITS_COLORS = {
        CardSuits.HEARTS: "red",
        CardSuits.DIAMONDS: "red",
        CardSuits.CLUBS: "blue",
        CardSuits.SPADES: "blue"
    }

    def __init__(self, value: CardValues, suit: CardSuits) -> None:
        self.base_value: int = value.value
        self.suit: CardSuits = suit
        self.hidden: bool = False

    @property
    def value(self) -> int:
        """Return the value of the card depending on its current state"""
        return 0 if self.hidden else self.base_value

    @property
    def display(self) -> str:
        """Return a string representation of the card dynamically"""
        if self.hidden:
            return colored("??", "grey")
        return colored(f"{self.base_value} {self.suit.value}", self.SUITS_COLORS[self.suit])

    def hide(self) -> None:
        """Hide the card"""
        self.hidden = True

    def reveal(self) -> None:
        """Reveal the card"""
        self.hidden = False

    def __str__(self) -> str:
        return self.display

    def __repr__(self) -> str:
        return self.display

    # --- Comparisons ---
    def __lt__(self, other) -> bool:
        return isinstance(other, Card) and self.value < other.value

    def __le__(self, other) -> bool:
        return isinstance(other, Card) and self.value <= other.value

    def __eq__(self, other) -> bool:
        return isinstance(other, Card) and self.value == other.value

    def __ge__(self, other) -> bool:
        return isinstance(other, Card) and self.value >= other.value

    def __gt__(self, other) -> bool:
        return isinstance(other, Card) and self.value > other.value

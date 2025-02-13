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
    ACE = 11 # Ace can be 1 or 11, it's decided later in the code


class CardSuits(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


# --- Classes ---
class Card:
    SUITS_COLORS = {CardSuits.HEARTS : "red", CardSuits.DIAMONDS : "red", CardSuits.CLUBS : "blue", CardSuits.SPADES : "blue"}
    
    def __init__(self, value: int, suit: CardSuits) -> None:
        self.value: int = value
        self.suit: CardSuits = suit
        self.hidden: bool = False
        self.strings: dict = {False : f"{colored(str(self.value) + ' ' + self.suit.value, Card.SUITS_COLORS[self.suit])}", True : f"{colored('??', 'grey')}"}

    def __str__(self) -> str:
        return self.strings[self.hidden]

    def __repr__(self) -> str:
        return self.strings[self.hidden]
    
    def __lt__(self, other) -> bool:
        return self.value < other.value
    
    def __le__(self, other) -> bool:
        return self.value <= other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value
    
    def __gt__(self, other) -> bool:
        return self.value > other.value


# --- Tests ---
if __name__ == "__main__":
    pass
    
    

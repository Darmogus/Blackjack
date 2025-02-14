# --- External libraries ---
from random import shuffle

# --- Internal libraries ---
from card import Card, CardValues, CardSuits


# --- Constants ---


# --- Classes ---
class Deck(list):
    def __init__(self):
        super().__init__()
        self.generate()
    
    def generate(self):
        """Generate a deck of 52 cards """
        for suit in CardSuits:
            for value in CardValues.__members__.values():
                self.append(Card(value, suit))

    def shuffle(self):
        """Shuffle the deck"""
        shuffle(self)
        
    def choose_card(self, card_index: int) -> Card | None:
        """Choose a card from the deck"""
        if len(self) < 1:
            return None
        if card_index <= 0:
            raise ValueError("card_index must be greater than 0")
        for i in range(card_index):
            card : Card = self[i % len(self)]
            if card:
                return card
        return None
    
    def pick_card(self, card_index: int) -> Card | None:
        """Pick a card and remove it from the deck"""
        card = self.choose_card(card_index)
        return self.pop(self.index(card))

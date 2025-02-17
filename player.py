# --- External librairies ---
from enum import Enum

# --- Internal librairies --- 
from card import Card
from stack import Stack
from deck import Deck


# --- Constants ---
class PlayerActions(Enum):
    HIT = "hit"             # Ask for another card
    STAND = "stand"         # Keep the current hand
    DOUBLE = "double"       # Double the bet and ask for another card
    SPLIT = "split"         # Split the hand into two hands (only if the two first cards are the same)
    SURRENDER = "surrender" # Give up and lose half of the bet


# --- Classes ---
class Player:
    def __init__(self, username: str, bet: int = 0, totalMoney: int = 1000) -> None:
        self.stacks: dict[int, Stack] = {0: Stack(bet)}
        self.totalMoney: int = totalMoney
        self.username: str = username
        
    @property
    def isPlaying(self):
        return any([stack.isPlaying for stack in self.stacks.values()])
    
    @property
    def isAlive(self):
        return any([stack.isAlive for stack in self.stacks.values()])
        
    def pick_card(self, deck: Deck, stackIndex: int = 0) -> None:
        """Pick a card and add it to a stack"""
        self.stacks[stackIndex].append(deck.pick_card(1))
        
    def get_possible_actions(self, stackIndex: int) -> list[PlayerActions]:
        """Return the possible actions for a given stack"""
        actions: list[PlayerActions] = [PlayerActions.HIT, PlayerActions.STAND]
        if len(self.stacks[stackIndex]) == 2:
            actions.append(PlayerActions.DOUBLE)
            if self.stacks[stackIndex].is_splitable() and self.totalMoney >= self.stacks[stackIndex].bet:
                actions.append(PlayerActions.SPLIT)
        return actions
        
    def choose_action(self, stack_index: int) -> PlayerActions:
        """Choose an action to do on a given stack"""
        possibleActions: list[PlayerActions] = self.get_possible_actions(stack_index)
        possibleActionsValues: list[str] = [action.value for action in possibleActions]
        while True:
            try:
                actionInput: str = str(input(f"Que voulez vous faire sur le stack n°{stack_index} ({', '.join(possibleActionsValues)}) : "))
                if actionInput in possibleActionsValues:
                    break
            except KeyboardInterrupt:
                print("Vous avez appuyé sur Ctrl+C")
                exit()
            except:
                print("Erreur de saisie")
            
        return PlayerActions(actionInput)
    
    def split(self):
        """Split the hand into two stacks"""
        newStack: Stack = Stack(bet=self.stacks[0].bet, card=self.stacks[0].pop(1))
        self.stacks[1] = newStack

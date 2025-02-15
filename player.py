# --- External librairies ---
from enum import Enum

# --- Internal librairies --- 
from card import Card


# --- Constants ---
class PlayerActions(Enum):
    HIT = "hit"             # Ask for another card
    STAND = "stand"         # Keep the current hand
    DOUBLE = "double"       # Double the bet and ask for another card
    SPLIT = "split"         # Split the hand into two hands (only if the two first cards are the same)
    SURRENDER = "surrender" # Give up and lose half of the bet


# --- Classes ---
class Player:
    def __init__(self, bet: int = 0, totalMoney: int = 1000) -> None:
        self.stacks: dict[list[Card | None]] = {0 : []}
        self.playingStacks: dict[int, bool] = {0 : True}
        self.totalMoney: int = totalMoney
        self.bets: dict[int] = {0 : bet}
        
    @property
    def isPlaying(self):
        return any(self.playingStacks.values())
        
    def get_possible_actions(self, stackIndex: int) -> list[PlayerActions]:
        """Return the possible actions for a given stack"""
        actions: list[PlayerActions] = [PlayerActions.HIT, PlayerActions.STAND]
        if len(self.stacks[stackIndex]) == 2:
            actions.append(PlayerActions.DOUBLE)
            if self.stacks[stackIndex][0].value == self.stacks[stackIndex][1].value and self.totalMoney >= self.bets[0]:
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
        self.stacks[1] = [self.stacks[0].pop(1)]
        self.playingStacks[1] = True
        self.bets[1] = self.bets[0]
        
    def end_stack(self, stack_index: int):
        """End a stack, the player can't play on it anymore, either because he surrendered, he died or because he got a blackjack"""
        self.playingStacks[stack_index] = False
        self.bets.pop(stack_index)

# --- External librairies ---
from enum import Enum

# --- Internal librairies --- 
from card import Card


# --- Constants ---
class PlayerActions(Enum):
    HIT = "hit"         # Ask for another card
    STAND = "stand"     # Keep the current hand
    DOUBLE = "double"   # Double the bet and ask for another card
    SPLIT = "split"     # Split the hand into two hands (only if the two first cards are the same)
    # SURRENDER = "surrender"
    
    @classmethod
    def values(self):
        return [action.value for action in PlayerActions] 


# --- Classes ---
class Player:
    def __init__(self, total_money: int = 1000, bet: int = 10) -> None:
        self.stacks: list[list[Card | None]] = [[]]
        self.total_money: int = total_money
        self.bets: list[int] = [bet]
        self.isPlaying: bool = True
        
    def get_possible_actions(self) -> list[PlayerActions]:
        actions: list[PlayerActions] = [PlayerActions.HIT, PlayerActions.STAND]
        if len(self.stacks[0]) == 2:
            actions.append(PlayerActions.DOUBLE)
            if self.stacks[0][0].value == self.stacks[0][1].value and self.total_money >= self.bets[0]:
                actions.append(PlayerActions.SPLIT)
        return actions
        
    def choose_action(self, stack_index: int) -> PlayerActions:       
        possibleActions: list[PlayerActions] = self.get_possible_actions()
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
        self.stacks.append([self.stacks[0].pop()])
        self.bets.append(self.bets[0])
        
    def remove_stack(self, stack_index: int):
        self.stacks.pop(stack_index)
        self.bets.pop(stack_index)
        
if __name__ == "__main__":
    P = Player()
    P.play_turn()
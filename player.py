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
    SURRENDER = "surrender"
    
    @classmethod
    def values(self):
        return [action.value for action in PlayerActions] 


# --- Classes ---
class Player:
    def __init__(self, totalMoney: int = 1000, bet: int = 10) -> None:
        self.stacks: dict[list[Card | None]] = {0 : []}
        self.playingStacks: dict[int, bool] = {0 : True}
        self.totalMoney: int = totalMoney
        self.bets: dict[int] = {0 : bet}
        
    @property
    def isPlaying(self):
        return any(self.playingStacks.values())
        
    def get_possible_actions(self, stackIndex: int) -> list[PlayerActions]:
        actions: list[PlayerActions] = [PlayerActions.HIT, PlayerActions.STAND]
        if len(self.stacks[stackIndex]) == 2:
            actions.append(PlayerActions.DOUBLE)
            if self.stacks[stackIndex][0].value == self.stacks[stackIndex][1].value and self.totalMoney >= self.bets[0]:
                actions.append(PlayerActions.SPLIT)
        return actions
        
    def choose_action(self, stack_index: int) -> PlayerActions:       
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
        self.stacks[1] = [self.stacks[0].pop(1)]
        self.playingStacks[1] = True
        self.bets[1] = self.bets[0]
        
    def end_stack(self, stack_index: int):
        self.playingStacks[stack_index] = False
        # self.bets.pop(stack_index)
        
if __name__ == "__main__":
    P = Player()
    P.play_turn()
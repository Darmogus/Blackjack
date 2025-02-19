
# --- Clases ---
class Stack(list):
    def __init__(self, bet: int) -> None:
        super().__init__()
        self.bet: int = bet
        self.isPlaying: bool = True
        
    @property
    def value(self) -> int:
        """Return the value of the stack"""
        return sum(card.value for card in self) 
    
    @property
    def isAlive(self) -> bool:
        """Return True if the stack is still alive (not dead or blackjack)"""
        return self.value < 21
    
    @property
    def cards(self) -> str:
        """Return the cards of the stack"""
        return " ".join(str(card) for card in self)
    
    def uncolor_cards(self):
        """Uncolor the cards of the stack"""
        for card in self:
            card.colored = False
    
    def is_splitable(self) -> bool:
        """Return True if the stack can be splitted"""
        return len(self) == 2 and self[0].value == self[1].value
    
    def reveal_cards(self):
        """Reveal the cards of the stack"""
        for card in self:
            card.isRevealed = True
    
    def end(self):
        """End the stack (for example if the player standed)"""
        self.isPlaying = False
        
    def kill(self):
        """Kill the stack (for example if the player surrendered, died or got a blackjack)"""
        self.isPlaying = False
        
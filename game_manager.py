# --- Internal libraries ---
from player import Player, PlayerActions
from deck import Deck

# --- External libraries ---

# --- Constants ---

# --- Classes ---
class GameManager:
    def __init__(self, player_nbr: int) -> None:
        self.players = [Player() for _ in range(player_nbr)]
        self.dealer = Player()
        self.deck = Deck()
        
        self.active_players = self.players.copy()
        
        self.deck.shuffle()
        self.deal_starting_cards()

    def deal_starting_cards(self):
        """Deal two cards to each player and the dealer"""
        for _ in range(2):
            for player in self.players:
                player.stacks[0].append(self.deck.pick_card(1))
            self.dealer.stacks[0].append(self.deck.pick_card(1))
        
        self.dealer.stacks[0][1].hidden = True # Hide the second card of the dealer

    def player_turn(self, player: Player):
        playerAction: PlayerActions = player.choose_action()
        
        match playerAction:
            case PlayerActions.HIT:
                player.stacks[0].append(self.deck.pick_card(1))
                
            case PlayerActions.STAND:
                player.isPlaying = False
            
            case PlayerActions.DOUBLE:
                pass
            
            case PlayerActions.SPLIT:
                player.split()
            
            case _:
                raise ValueError("Invalid action")
            
    def is_dead(self, player: Player, stack_index: int) -> bool:
        try:
            return sum([card.value for card in player.stacks[stack_index]]) > 21
        except IndexError:
            raise ValueError("Invalid stack index")

    def display_table(self):
        for player in self.players:
            for i in range(len(player.stacks)):
                print(f'Stack n°{i} : {player.stacks[i]} Total : {sum([card.value for card in player.stacks[i]])} | Bet : {player.bets[i]}€')
        print(f'Stack : {self.dealer.stacks[0]} Total : {sum([card.value for card in self.dealer.stacks[0]])}')

    def play(self):
        self.display_table()
        for player in self.players:
            player.isPlaying = True
            while player.isPlaying:
                self.player_turn(player)
                self.display_table()
                if self.is_dead(player, 0):
                    self.active_players.remove(player)
                    player.isPlaying = False
                    print("Busted")
                    break
        print("Dealer turn")
        self.dealer.stacks[0][1].hidden = False

        
# --- Tests ---
if __name__ == '__main__':
    game = GameManager(1)
    game.play()
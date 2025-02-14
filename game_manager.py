# --- External libraries ---
import os
from termcolor import colored

# --- Internal libraries ---
from player import Player, PlayerActions
from deck import Deck

# --- Constants ---

# --- Classes ---
class GameManager:
    def __init__(self, player_nbr: int) -> None:
        self.players = [Player() for _ in range(player_nbr)]
        self.dealer = Player()
        self.deck = Deck()
            
        self.deck.shuffle()
        self.deal_starting_cards()
        
    @property
    def alive_players(self):
        return [player for player in self.players 
                if player.total_money > 0 
                and any(sum(card.value for card in stack) < 22 for stack in player.stacks)]

    def deal_starting_cards(self):
        """Deal two cards to each player and the dealer"""
        for _ in range(2):
            for player in self.players:
                player.stacks[0].append(self.deck.pick_card(1))
            self.dealer.stacks[0].append(self.deck.pick_card(1))
        
        self.dealer.stacks[0][1].hidden = True # Hide the second card of the dealer

    def player_turn(self, player: Player, stack_index: int):
        playerAction: PlayerActions = player.choose_action(stack_index)
        
        match playerAction:
            case PlayerActions.HIT:
                player.stacks[0].append(self.deck.pick_card(1))
                
            case PlayerActions.STAND:
                pass            
            case PlayerActions.DOUBLE:
                pass
            
            case PlayerActions.SPLIT:
                player.split()
            
            case _:
                raise ValueError("Invalid action")
         
    def dealer_turn(self):
        print("Dealer's turn")
        self.dealer.stacks[0][1].hidden = False
        while sum([card.value for card in self.dealer.stacks[0]]) < 17:
            self.dealer.stacks[0].append(self.deck.pick_card(1))
            
    def compare_hands(self):
        dealer_total = sum([card.value for card in self.dealer.stacks[0]])
        if dealer_total > 21:
            print("Dealer is dead")
            for player in self.alive_players:
                for stack in player.stacks:
                    player.total_money += player.bets[player.stacks.index(stack)]
                    print(colored(f"+ {player.bets[player.stacks.index(stack)]}€", 'green'))
            return
        
        for player in self.alive_players:
            for stack in player.stacks:
                player_total = sum([card.value for card in stack])
                if player_total > dealer_total:
                    player.total_money += player.bets[player.stacks.index(stack)]
                    print(colored(f"+ {player.bets[player.stacks.index(stack)]}€", 'green'))
                elif player_total < dealer_total:
                    player.total_money -= player.bets[player.stacks.index(stack)]
                    print(colored(f"- {player.bets[player.stacks.index(stack)]}€", 'red'))
                else:
                    print("It's a tie, no money won or lost.")
            
    def is_blackjack(self, player: Player, stack_index: int):
        if sum([card.value for card in player.stacks[stack_index]]) == 21:
            print("Blackjack")
            if len(player.stacks[stack_index]) == 2:
                player.total_money += player.bets[stack_index] * 1.5
                print(colored(f"+ {player.bets[stack_index] * 1.5}€", 'green'))
            else:
                player.total_money += player.bets[stack_index]
                print(colored(f"+ {player.bets[stack_index]}€", 'green'))
            return True
        return False
            
    def is_dead(self, player: Player, stack_index: int) -> bool:
        if sum([card.value for card in player.stacks[stack_index]]) > 21:
            print("Dead")
            return True 
    
    def display_table(self):
        for player in self.alive_players:
            for i in range(len(player.stacks)):
                print(f"Stack n°{i} : {player.stacks[i]} Total : {sum([card.value for card in player.stacks[i]])} | Bet : {player.bets[i]}€")
        print(f"Dealer's hand : {self.dealer.stacks[0]} Total : {sum([card.value for card in self.dealer.stacks[0]])}")

    def play(self):
        self.display_table()
        
        for player in self.players:
            player.isPlaying = True
            while player.isPlaying:
                for ind, stack in enumerate(player.stacks[:]):                    
                    if self.is_blackjack(player, ind):
                        break
                    
                    self.player_turn(player, ind)
                    self.display_table()
                    
                    if self.is_blackjack(player, ind):
                        continue
                    
                    if self.is_dead(player, ind):
                        continue
                
                if len(player.stacks) == 0 or len(player.stacks) == 2:
                    player.isPlaying = False
                
        self.dealer_turn()
        self.display_table()
        self.compare_hands()
                    
        
# --- Tests ---
if __name__ == '__main__':
    game = GameManager(1)
    game.play()
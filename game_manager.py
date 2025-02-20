# --- External libraries ---
import os
from time import sleep
from termcolor import colored

# --- Internal libraries ---
from player import Player, PlayerActions
from deck import Deck
from card import Card


# --- Classes ---
class GameManager:
    def __init__(self, player_nbr: int) -> None:
        self.players = [Player(i+1) for i in range(player_nbr)]
        self.dealer = Player('Dealer')
        self.deck = Deck()
            
        os.system('cls')
        
    @property
    def alivePlayers(self) -> list[Player]:
        """Return the players who are still alive""" # A player that got a blackjack is not considered alive
        return [player for player in self.players 
                if player.totalMoney > 0
                and player.isAlive]
        
    @property
    def richPlayers(self) -> list[Player]:
        """Return the players who still have money"""
        return [player for player in self.players if player.totalMoney > 0]
        
    def end_game(self) -> None:
        """End the game"""
        os.system('cls')
        print(colored("\n==================== END OF GAME ====================", "yellow"))
        print(colored("\n🏁 End of the game !", "magenta", attrs=['bold']))
        for player in self.players:
            print(colored(f"\n👤 Player {player.username} - Money: {player.totalMoney}€", "blue"))
        print(colored("\n======================================================", "yellow"))
        exit()
        
    def announce_player_win(self, player: Player, amount: int) -> None: # TODO : choisir si on affiche quel stack gagne quoi ou si l'on fait le total
        """Announce the win of a player"""
        print(colored(f"✅ Player {player.username} | + {amount}€", 'green'))
        
    def announce_player_loss(self, player: Player, amount: int) -> None:
        """Announce the loss of a player"""
        print(colored(f"❌ Player {player.username} | - {amount}€", 'red'))
        
    def announce_player_tie(self, player: Player) -> None:
        """Announce the tie of a player"""
        print(colored(f"🔵 Player {player.username} | ~ {0}€", 'blue'))

    def player_pick_card(self, player: Player, stackIndex: int = 0) -> None:
        """Pick a card for a player"""
        card: Card = self.deck.pick_card(1)
        # Ace can be 1 or 11
        if card.base_value == 11 and player.stacks[stackIndex].value + 11 > 21:
            card.base_value = 1
        print(stackIndex, player.stacks)
        player.stacks[stackIndex].append(card)

    def deal_starting_cards(self) -> None:
        """Deal two cards to each player and the dealer"""
        self.dealer.set_initial_stack(0)
        for _ in range(2):
            for player in self.players:
                self.player_pick_card(player)
            self.player_pick_card(self.dealer)
        
        self.dealer.stacks[0][1].hide()
        
    def set_bets(self) -> None:
        """Set the starting bets of each player with a visual representation"""
        while True:
            os.system('cls')
            print(colored("\n==================== BETTING TABLE ====================", "yellow"))

            # Display the players and their money
            for ind, player in enumerate(self.players):
                print(colored(f"\n👤 Player {ind} - Money: {player.totalMoney}€", "blue"))

            print(colored("\n======================================================", "yellow"))

            # Bet input
            for ind, player in enumerate(self.players):
                while True:
                    try:
                        bet = int(input(colored(f"\n🎲 Player {ind} - Enter your bet: ", "cyan")))
                        
                        if bet > player.totalMoney:
                            print(colored("❌ You don't have enough money.", "red"))
                            continue
                        
                        player.set_initial_stack(bet)
                        break
                    except ValueError:
                        print(colored("❌ Please enter a valid number.", "red"))
                        
                    except KeyboardInterrupt:
                        self.end_game()

            os.system('cls')
            break


    def player_turn(self, player: Player, stackIndex: int) -> None:
        """Play the turn of a player"""
        print(colored(f"\n🎮 Tour de Joueur {player.username} !", "cyan"))
        playerAction: PlayerActions = player.choose_action(stackIndex)
        
        match playerAction:
            case PlayerActions.HIT:
                self.player_pick_card(player, stackIndex)
                
            case PlayerActions.STAND:
                player.stacks[stackIndex].end()
                     
            case PlayerActions.DOUBLE:
                self.player_pick_card(player, stackIndex)
                player.stacks[stackIndex].bet *= 2
                player.stacks[stackIndex].end()
            
            case PlayerActions.SPLIT:
                player.split()
                
            case PlayerActions.SURRENDER:
                player.totalMoney -= player.stacks[stackIndex].bet // 2
                player.stacks[stackIndex].kill()
                
            case None:
                self.end_game()
                
            case _:
                raise ValueError("Invalid action")
         
    def dealer_turn(self) -> None:
        """Play the dealer turn"""
        self.dealer.stacks[0][1].reveal()
        self.display_table()
        print(colored("\n🏆 Tour du croupier !", "yellow"))

        sleep(1)
        while self.dealer.stacks[0].value < 17:
            self.player_pick_card(self.dealer)
            self.display_table()
            print(colored("\n🏆 Tour du croupier !", "yellow"))
            sleep(1)
            
        if self.dealer.stacks[0].value == 21:
            print(colored("\n🔥 Blackjack !", "green"))
            return
        
    def dealer_win(self) -> None:
        """The dealer wins the game"""
        self.display_table()
        print(colored("\n🏆 The dealer won !", "yellow"))
        for player in self.players:
            for stackIndex, _ in player.stacks:
                moneyAmount: int = player.stacks[stackIndex].bet
                self.announce_player_loss(player, moneyAmount)
                return
    
    def dealer_lose(self) -> None:
        """The dealer loses the game"""
        print(colored("❌ Le croupier a dépassé 21 !", "red"))
        for player in self.players:
            for stack in player.stacks.values():
                moneyAmount: int = stack.bet
                if player in self.alivePlayers:
                    self.announce_player_win(player, moneyAmount)
                else:
                    if stack.value == 21:
                        self.announce_player_win(player, moneyAmount)
                    else:
                        self.announce_player_loss(player, moneyAmount)
                            
    def compare_hands(self, dealerTotal) -> None:
        """Compare the hands of the players and the dealer"""
        for player in self.players:
            for _, stack in player.stacks.items():
                playerTotal = stack.value
                moneyAmount: int = stack.bet
                
                if not player in self.alivePlayers:
                    if stack.value == 21:
                        self.announce_player_win(player, stack.bet)
                    else:
                        self.announce_player_loss(player, stack.bet)
                    
                elif playerTotal > dealerTotal:
                    player.totalMoney += moneyAmount
                    self.announce_player_win(player, moneyAmount)
                elif playerTotal < dealerTotal:
                    player.totalMoney -= moneyAmount
                    self.announce_player_loss(player, moneyAmount)
                else:
                    self.announce_player_tie(player)
    
    def comparison_turn(self) -> None:
        """Compar the hands of the players and the dealer"""
        self.display_table()
        print(colored("\n💰 Final result :", "magenta", attrs=['bold']))

        dealerTotal = self.dealer.stacks[0].value
        if len(self.alivePlayers) == 0:
            self.dealer_win()
            return

        if dealerTotal > 21:
            self.dealer_lose()
            return
        
        self.compare_hands(dealerTotal)

    def is_blackjack(self, player: Player, stackIndex: int) -> bool:
        if player.stacks[stackIndex].value == 21:
            player.stacks[stackIndex].kill()
            return True
        return False
            
    def is_dead(self, player: Player, stackIndex: int) -> bool:  
        if player.stacks[stackIndex].value > 21:
            player.stacks[stackIndex].kill()
            return True
        return False
            
    def process_blackjack(self, player: Player, stackIndex: int) -> None:
        """Process the blackjack of a player"""
        betAmount: int = player.stacks[stackIndex].bet
        print(colored("\n🔥 Blackjack !", "green"))
        if len(player.stacks[stackIndex]) == 2:
            moneyAmount: int = betAmount * 1.5
            self.announce_player_win(player, moneyAmount)
        else:
            moneyAmount: int = betAmount
            self.announce_player_win(player, moneyAmount)
        player.stacks[stackIndex].kill()
            
    def process_dead(self, player: Player, stackIndex: int) -> None:
        """Process the dead of a player"""
        print(colored(f"\n💀 Player {player.username} | Stack n°{stackIndex} of  exceeded 21!", "red"))
        player.totalMoney -= player.stacks[stackIndex].bet
        player.stacks[stackIndex].kill()
    
    def display_table(self) -> None:
        """Display the game table"""
        os.system('cls')
        print(colored("\n==================== GAME TABLE ====================", "yellow"))

        # Dealer display
        print(colored("\n🃏 Dealer's hand:", "red"))
        dealer_cards = self.dealer.stacks[0].cards
        dealer_total = self.dealer.stacks[0].value
        print(f"Cartes: {dealer_cards} | Total: {dealer_total}")

        print(colored("\n🎭 Players:", "cyan"))

        # Players display
        for i, player in enumerate(self.players, 1):
            print(colored(f"\n👤 Player {i} - Money: {player.totalMoney}€", "blue"))
            for stackIndex, stack in player.stacks.items():
                if stack.value == 21:
                    stack.uncolor_cards()
                    print(colored(f"  - Stack n°{stackIndex}: {stack.cards} | Total: {stack.value} | Bet: {stack.bet}€", "green"))
                    continue
                if stack.value > 21:
                    stack.uncolor_cards()
                    print(colored(f"  - Stack n°{stackIndex}: {stack.cards} | Total: {stack.value} | Bet: {stack.bet}€", "red"))
                    continue
                cards = stack.cards
                total = stack.value
                bet = stack.bet
                print(f"  - Stack n°{stackIndex}: {cards} | Total: {total} | Bet: {bet}€")
        print(colored("\n======================================================", "yellow"))

    def reset_players(self):
        self.dealer.reset_stacks()
        for player in self.players:
            player.reset_stacks()

    def setup_game(self):
        self.deck.generate()
        self.deck.shuffle()
        self.set_bets()
        self.deal_starting_cards()
        
    def play(self):
        """Play the game"""
        self.setup_game()
        for player in self.players:
            while player.isPlaying:
                try:
                    for stackIndex, stack in player.stacks.items():
                        while stack.isPlaying:
                            if self.is_blackjack(player, stackIndex):
                                break
                            if self.is_dead(player, stackIndex):
                                break
                            
                            self.display_table()
                            self.player_turn(player, stackIndex)
                            os.system('cls')
                

   
                    os.system('cls')
                    self.display_table()
                    if self.is_blackjack(player, stackIndex):
                        self.process_blackjack(player, stackIndex)
                    elif self.is_dead(player, stackIndex):
                        self.process_dead(player, stackIndex)
                            
                except KeyboardInterrupt:
                   self.end_game()
                
            input("\nPress Enter to continue...")
            os.system('cls')
        
        if self.alivePlayers:
            self.display_table()
            sleep(0.5)
            self.dealer_turn()
            sleep(1)
            self.comparison_turn()
            
    def run(self):
        """Run the game"""
        while len(self.richPlayers) > 0:
            self.play()
            input("\nPress Enter to continue...")
        self.end_game()
                    

# --- Tests ---
if __name__ == '__main__':
    game = GameManager(3)
    game.run()

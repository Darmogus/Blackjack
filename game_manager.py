# --- External libraries ---
import os
from time import sleep
from termcolor import colored

# --- Internal libraries ---
from player import Player, PlayerActions
from deck import Deck


# --- Classes ---
class GameManager:
    def __init__(self, player_nbr: int) -> None:
        self.players = [Player() for _ in range(player_nbr)]
        self.dealer = Player()
        self.deck = Deck()
            
        os.system('cls')
        
        self.deck.shuffle()
        self.deal_starting_cards()
        self.set_starting_bets()
        
    @property
    def alive_players(self) -> list[Player]:
        """Return the players who are still alive""" # A player that got a blackjack is not considered alive
        return [player for player in self.players 
                if player.totalMoney > 0 
                and player.isAlive]

    def deal_starting_cards(self) -> None:
        """Deal two cards to each player and the dealer"""
        for _ in range(2):
            for player in self.players:
                player.stacks[0].append(self.deck.pick_card(1))
            self.dealer.stacks[0].append(self.deck.pick_card(1))
        
        self.dealer.stacks[0][1].hide()
        
    def set_starting_bets(self) -> None:
        """Set the starting bets of each player with a visual representation"""
        while True:
            os.system('cls')  # Efface l'écran avant d'afficher la table
            print(colored("\n==================== BETTING TABLE ====================", "yellow"))

            # Affichage des joueurs et de leur argent
            for ind, player in enumerate(self.players):
                if player.stacks[0].bet == 0:
                    print(colored(f"\n👤 Player {ind} - Money: {player.totalMoney}€", "blue"))
                else:
                    print(colored(f"\n👤 Player {ind} - Money: {player.totalMoney}€ - Bet: {player.bets[0]}€", "blue"))

            print(colored("\n======================================================", "yellow"))

            # Demande les mises
            for ind, player in enumerate(self.players):
                while True:
                    try:
                        bet = int(input(colored(f"\n🎲 Player {ind} - Enter your bet: ", "cyan")))
                        
                        if bet > player.totalMoney:
                            print(colored("❌ You don't have enough money.", "red"))
                            continue
                        
                        player.stacks[0].bet = bet
                        break
                    except ValueError:
                        print(colored("❌ Please enter a valid number.", "red"))
                        
                    except KeyboardInterrupt:
                        print("You pressed Ctrl+C")
                        exit()

            os.system('cls')  # Efface l'écran après la saisie des mises
            break


    def player_turn(self, player: Player, stackIndex: int) -> None:
        """Play the turn of a player"""
        print(colored("\n🎮 Tour du joueur !", "cyan"))
        playerAction: PlayerActions = player.choose_action(stackIndex)
        
        match playerAction:
            case PlayerActions.HIT:
                player.stacks[stackIndex].append(self.deck.pick_card(1))
                
            case PlayerActions.STAND:
                player.stacks[stackIndex].end()
                     
            case PlayerActions.DOUBLE:
                player.stacks[stackIndex].bet *= 2
                player.stacks[stackIndex].append(self.deck.pick_card(1))
                player.stacks[stackIndex].end()
            
            case PlayerActions.SPLIT:
                player.split()
                
            case PlayerActions.SURRENDER:
                player.totalMoney -= player.stacks[stackIndex].bet // 2
                player.stacks[stackIndex].kill()
            case _:
                raise ValueError("Invalid action")
         
    def dealer_turn(self) -> None: 
        """Play the dealer turn"""
        print(colored("\n🏆 Tour du croupier !", "yellow"))
        self.dealer.stacks[0][1].reveal()

        sleep(1)
        while sum([card.value for card in self.dealer.stacks[0]]) < 17:
            os.system('cls')
            self.dealer.pick_card(self.deck)
            self.display_table()
            sleep(1)
            
        if sum([card.value for card in self.dealer.stacks[0]]) == 21:
            print(colored("\n🔥 Blackjack !", "green"))
            return
        
    def dealer_win(self) -> None:
        """The dealer wins the game"""
        self.display_table()
        print(colored("\n🏆 The dealer won !", "yellow"))
        for player in self.players:
            for stackIndex, _ in player.stacks:
                print(colored(f"❌ - {player.stacks[stackIndex].bet}€", 'red'))
                return
    
    def dealer_lose(self) -> None:
        """The dealer loses the game"""
        print(colored("❌ Le croupier a dépassé 21 !", "red"))
        for player in self.alive_players:
            for stackIndex, _ in player.stacks.items():
                moneyAmount: int = player.stacks[stackIndex].bet
                player.totalMoney += moneyAmount
                print(colored(f"✅ + {moneyAmount}€", 'green'))
            
    def compare_hands(self, dealerTotal) -> None: # TODO : afficher qui gagne quoi (actuellement affiche juste le gain ou la perte)
        """Compare the hands of the players and the dealer"""
        for player in self.alive_players:
            for stackIndex, stack in player.stacks.items():
                playerTotal = stack.value
                moneyAmount: int = stack.bet
                
                if playerTotal > dealerTotal:
                    player.totalMoney += moneyAmount
                    print(colored(f"✅ + {moneyAmount}€", 'green'))
                elif playerTotal < dealerTotal:
                    player.totalMoney -= moneyAmount
                    print(colored(f"❌ - {moneyAmount}€", 'red'))
                else:
                    print(colored("🔄 It's a tie, nobody wins.", "blue"))  
    
    def comparison_turn(self) -> None:
        """Compar the hands of the players and the dealer"""
        os.system('cls')
        dealerTotal = self.dealer.stacks[0].value
        print(colored("\n💰 Final result :", "magenta"))

        if len(self.alive_players) == 0:
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
            
    def process_blackjack(self, player: Player, stackIndex: int) -> None: # TODO : régler les ordres d'affiche (voire les refaire complètement) 
                                                                     # actuellement, le blackjack s'affiche au dessus de la table suivante
        """Process the blackjack of a player"""
        betAmount: int = player.stacks[stackIndex].bet
        print(colored("\n🔥 Blackjack !", "green"))
        if len(player.stacks[stackIndex]) == 2:
            player.totalMoney += betAmount * 1.5
            print(colored(f"✅ + {betAmount * 1.5}€", 'green'))
        else:
            player.totalMoney += betAmount
            print(colored(f"✅ + {betAmount}€", 'green'))
        player.stacks[stackIndex].kill()
            
    def process_dead(self, player: Player, stackIndex: int) -> None:
        """Process the dead of a player"""
        betAmount: int = player.stacks[stackIndex].bet
        print(colored(f"\n💀 Stack n°{stackIndex} exceeded 21!", "red"))
        print(colored(f"❌ - {betAmount}€", 'red'))
        player.totalMoney -= betAmount
        player.stacks[stackIndex].kill()
    
    def display_table(self) -> None: # TODO : Peut être faire en sorte que une ligne précise à qui est le tour de jouer (joueur ou croupier)
        """Display the game table"""
        print(colored("\n==================== GAME TABLE ====================", "yellow"))

        # Affichage du croupier
        print(colored("\n🃏 Dealer's hand:", "red"))
        dealer_cards = self.dealer.stacks[0].cards
        dealer_total = self.dealer.stacks[0].value
        print(f"Cartes: {dealer_cards} | Total: {dealer_total}")

        print(colored("\n🎭 Players:", "cyan"))

        # Affichage des joueurs
        for i, player in enumerate(self.players, 1):
            print(colored(f"\n👤 Player {i} - Money: {player.totalMoney}€", "blue"))
            for stackIndex, stack in player.stacks.items():
                if stack.value == 21:
                    continue
                cards = stack.cards
                total = stack.value
                bet = stack.bet
                print(f"  - Stack n°{stackIndex}: {cards} | Total: {total} | Bet: {bet}€")
        print(colored("\n======================================================", "yellow"))

    def play(self):
        """Play the game"""
        for player in self.players:
            while player.isPlaying:
                try:
                    for stackIndex, stack in player.stacks.items():
                        while stack.isPlaying:
                            if self.is_blackjack(player, stackIndex): # TODO : afficher le blackjack (le stack) juste avant la fin de game (actuellement n'affiche rien)
                                break
                            if self.is_dead(player, stackIndex):
                                break
                            
                            self.display_table()
                            self.player_turn(player, stackIndex)
                            os.system('cls')
                
                except KeyboardInterrupt:
                    print("Bye !")
                    exit()
   
            os.system('cls')
            self.display_table()
            if self.is_blackjack(player, stackIndex):
                self.process_blackjack(player, stackIndex)
            elif self.is_dead(player, stackIndex):
                self.process_dead(player, stackIndex)
                
            input("\nPress Enter to continue...")
            os.system('cls')
        
        if self.alive_players: # TODO : quand les 3 joueurs ont fini de jouer, le jeu rentre dans une boucle infinie
            self.display_table()
            sleep(0.5)
            self.dealer_turn()
            sleep(1)
            self.comparison_turn()
                    

# --- Tests ---
if __name__ == '__main__':
    game = GameManager(3)
    game.play()

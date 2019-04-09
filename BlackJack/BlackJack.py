# BlackJack 0.2
# =============

# Blackjack game created to help me learn python.
# The goal is make a program that can play by it's own
# and show the statistics envolved.

# Features:
# - hability to use real decks with cards and suits
# - Can use as many decks as desired in a given match
# - The decks are consumed by each match and when its near exaustion,
#   the dealer get new decks
# - able to use different algoritms to decide if hit ot not
# - can look to the cards in the dealer(player "sees" dealer hand)
# - Possible to run tousands of simulations
# - Multiprocessing(give a number of simulations to a process and create several processes)
# - TODO: Implement double down, surrender, insurance, the amout payied for insurance, the amout payed by blackjack .. all in parameters
# - DONE -- Fix the order of the dealed cards. They have an order... and it must be followed
# - TODO: make this program be able to play against flash sites with bj games
# - TODO: Implement spliting of cards
# - TODO: Implement betting
# - DONE -- Implement push(tie, when neither the player or dealer wins. Today when there is a tie, the dealer wins)
# - TODO: Implement algorigm of Machine Learning (this is the main original goal)
# - TODO: Implement algoritm of Card Counting (Hi-Lo ? Must me able to do 2 types of CC: One like the real world and other with simulated real decks "in mind")
# - TODO: Implement Multithreading to compare performance. Probably worse
# - TODO: Implement Multiprocessing by NOT using a Pool .. to compare performance
# - TODO: export lots os data and shit to use with Jupyter and Plot and Numby and etc
# - TODO: Implement game against a human (1 and 2 players ?)
# - TODO: Create a GUI ?
# - TODO: Find a way to show progress when in multiprocessing mode
# - TODO: Support more then 1 player.
# - TODO: Implement some way of measuring the speed, like 2323 matches / sec


import random as rnd
import multiprocessing

from time import sleep, time

from bib_support import print_inline, ls, get_card_val
from BlackJack_Alg import blackjack_alg_50X50, blackjack_alg_WIKIPEDIA_BLACKJACK, blackjack_alg_MURCH, blackjack_alg_SIMPLE


class GamePlayer:

    def __init__(self, _name: str, _type: str = "PLAYER", _algoritm: str = "50X50", _cards: list = [], _known_dealer_cards: list = [], _start_money: float = 1000.0):
        self.name = _name
        self.type = _type
        self.cards = _cards
        self.algoritm = _algoritm
        self.known_dealer_cards = _known_dealer_cards
        self.start_money = _start_money
        self.final_money = _start_money
        self.actual_bet = 0

    def hit(self, _deck_used: list, _card: list = []) -> None:

        if _card == []:
            self.cards.append(get_card_from_deck(_deck_used))
        else:
            self.cards.append(_card)

    def print_hand(self) -> list:

        # return [ x[0] + "|" + x[1] + "|" + str(get_card_val(x[0])) for x in self.cards ]
        # return [ x[0] + "|" + x[1] for x in self.cards ]
        # return [ x[0] + " " + str(get_card_val(x[0])) +  x[1] for x in self.cards ]

        return [x[0] + x[1] for x in self.cards]

    def get_card_sum(self) -> int:

        num_of_aces = len([x[0] for x in self.cards if x[0] == "A"])

        if num_of_aces <= 1:

            value_for_ace = 11

            for card in self.cards:

                if get_card_val(card[0]) >= 11:
                    value_for_ace = 1

        else:
            value_for_ace = 1

        sum_ = 0

        for card in self.cards:

            if get_card_val(card[0]) == 1:

                sum_ += value_for_ace

            else:
                sum_ += get_card_val(card[0])

        return sum_

    def should_hit(self, _force: bool = None) -> bool:

        ret = False

        if _force is None:

            if self.algoritm not in ["NEVER", "ALWAYS", "50X50", "WIKIPEDIA_BLACKJACK", "MURCH"]:
                self.algoritm = "50X50"

            if self.algoritm == "50X50":
                ret = blackjack_alg_50X50()

            elif self.algoritm == "WIKIPEDIA_BLACKJACK":
                ret = blackjack_alg_WIKIPEDIA_BLACKJACK(self)

            elif self.algoritm == "MURCH":
                ret = blackjack_alg_MURCH(self)

            elif self.algoritm == "SIMPLE":
                ret = blackjack_alg_SIMPLE()

            elif self.algoritm == "NEVER":
                ret = False

            elif self.algoritm == "ALWAYS":
                ret = True

            # if its the dealer, the rules says it must hit if has 16 or less
            if self.type == "DEALER":
                if self.algoritm not in ["NEVER", "ALWAYS"]:
                    if self.get_card_sum() <= 16:
                        ret = True

            # if has 21 or more, always say no to hit
            if self.get_card_sum() >= 21:
                if self.algoritm not in ["NEVER", "ALWAYS"]:
                    ret = False

            return ret

        else:
            return _force

    def define_bet(self) -> float:
        return 10


def get_card_from_deck(deck: list, forceValue: str = None) -> list:
    if forceValue is None:
        return deck.pop()
    else:
        return [forceValue, "♥"]


def new_deck(shuffled: bool = True, number_of_decks_used: int = 1) -> list:

    # _deck = [ ["A", "OUROS"], ["7", "ESPADAS"] ]

    values = [str(x) for x in range(2, 11)] + ["J", "Q", "K", "A"]

    # suits = ["OUROS", "ESPADAS", "COPAS", "PAUS"] # ♥♦♣♠
    suits = ["♦", "♠", "♥", "♣"]  # ♥♦♣♠

    deck_final = []

    for x in range(1, number_of_decks_used + 1):
        deck = [[value, suit] for value in values for suit in suits]

        deck_final = deck_final + deck

    if shuffled == True:
        rnd.shuffle(deck_final)

    return deck_final


def run_match(deck: list, use_betting: bool = False) -> str:

    winner = ""

    #  create player and dealer
    player = GamePlayer(_name="Murch", _algoritm="WIKIPEDIA_BLACKJACK", _cards=[])
    dealer = GamePlayer(_name="Blacu Jacku", _type="DEALER", _cards=[])

    # if we are using bets, then, place bet
    if use_betting is True:
        player.actual_bet = player.define_bet()

    # Players get 1 card
    player.hit(deck)

    # Dealer get 1 card face up
    dealer.hit(deck)

    # dealer reveals their first card to players
    player.known_dealer_cards = dealer.cards[0]

    # Players get 1 more card
    player.hit(deck)

    # Dealer get 1 more card face down
    dealer.hit(deck)

    # player = GamePlayer(_name="Murch", _algoritm = "MURCH", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name="Murch", _algoritm = "SIMPLE", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck), get_card_from_deck(deck) ])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck, "K"), get_card_from_deck(deck, "8") ])

    ls("=== MATCH ===========================================")
    ls("Player INIT hand:", player.print_hand(), player.get_card_sum())
    ls("dealer  INIT hand:", dealer.print_hand(), dealer.get_card_sum())

    ls("-----------------------------------------------------")

    turn = "PLAYER"

    while turn == "PLAYER":

        check_hit = player.should_hit()

        if check_hit is True:
            player.hit(deck)

        ls("PLAYER: check_hit =", check_hit, "| Cartas: ", player.print_hand(), player.get_card_sum())

        if player.get_card_sum() > 21:
            turn = "END"
            winner = "DEALER"

            if use_betting is True:
                dealer.final_money = dealer.final_money + player.actual_bet
                player.final_money = player.final_money - player.actual_bet
                player.actual_bet = 0

            ls("player exploded!")

        else:
            if check_hit is False:
                turn = "DEALER"

    while turn == "DEALER":

        check_hit = dealer.should_hit()

        if check_hit is True:
            dealer.hit(deck)

        ls("DEALER: check_hit =", check_hit, "| Cartas: ", dealer.print_hand(), dealer.get_card_sum())

        if dealer.get_card_sum() > 21:
            turn = "END"
            winner = "PLAYER"

            if use_betting is True:
                dealer.final_money = dealer.final_money - player.actual_bet
                player.final_money = player.final_money + player.actual_bet
                player.actual_bet = 0

            ls("dealer exploded!")

        else:
            if check_hit is False:
                turn = "END"

        # ls("-----------------------------------------------------")

    if winner == "":
        if dealer.get_card_sum() == player.get_card_sum():
            winner = "PUSH"
            player.actual_bet = 0

        elif dealer.get_card_sum() > player.get_card_sum():
            winner = "DEALER"

            if use_betting is True:
                dealer.final_money = dealer.final_money + player.actual_bet
                player.final_money = player.final_money - player.actual_bet
                player.actual_bet = 0

        elif dealer.get_card_sum() < player.get_card_sum():
            winner = "PLAYER"

            if use_betting is True:
                dealer.final_money = dealer.final_money - player.actual_bet
                player.final_money = player.final_money + player.actual_bet
                player.actual_bet = 0

    ls("Player FINAL hand:", player.print_hand(), player.get_card_sum())
    ls("dealer  FINAL hand:", dealer.print_hand(), dealer.get_card_sum())
    ls("WINNER:", winner)

    ls("=== FINAL ===========================================")

    ls("\n\n")
    # print(player.should_hit())

    # print(gPlayer1.cards)
    #
    # gPlayer1.add_card()
    #
    # print(gPlayer1.cards)

    return winner


# def simulate_matches(num_matches: int = 1, processing_mode: str = "NORMAL") -> tuple:
def simulate_matches(params: list = [1, "NORMAL", False]) -> tuple:

    total_win_player = 0
    total_win_dealer = 0
    total_win_push = 0

    number_of_decks = 6

    num_matches = params[0]
    processing_mode = params[1]
    use_betting = params[2]

    current_deck = new_deck(number_of_decks_used=number_of_decks)  # according to the rules, 8 decks are used

    for x in range(0, num_matches):

        # if there are less then 20 cards in deck, get new decks
        if len(current_deck) <= 20:
            current_deck = new_deck(number_of_decks_used=number_of_decks)

        # print(current_deck)

        # as the rules say, shuffle after every match
        rnd.shuffle(current_deck)

        winner = run_match(current_deck, use_betting)

        if winner == "PLAYER":
            total_win_player = total_win_player + 1

        elif winner == "DEALER":
            total_win_dealer = total_win_dealer + 1

        elif winner == "PUSH":
            total_win_push = total_win_push + 1

        if x > 9:
            win_ratio_player = (total_win_player * 100) / x
            win_ratio_dealer = (total_win_dealer * 100) / x
            win_ratio_push = (total_win_push * 100) / x

            # check_sum = win_ratio_player + win_ratio_dealer + win_ratio_push

            line = "Real time: Win Ratio in " + "{:06d}".format(x + 1) + " games (player x dealer x push): " \
                + "{:.8f}".format(win_ratio_player) + ", " \
                + "{:.8f}".format(win_ratio_dealer) + ", " \
                + "{:.8f}".format(win_ratio_push) \
                + " -- Deck size: " + str(len(current_deck))

            if processing_mode in ["NORMAL"]:
                print_inline(line)

    if num_matches > 10:
        if processing_mode in ["NORMAL"]:
            print("")

    win_ratio_player = (total_win_player * 100) / num_matches
    win_ratio_dealer = (total_win_dealer * 100) / num_matches
    win_ratio_push = (total_win_push * 100) / num_matches

    # check_sum = win_ratio_player + win_ratio_dealer + win_ratio_push

    return win_ratio_player, win_ratio_dealer, win_ratio_push


def Main() -> None:
    """
    Main function
    """

    num_matches = 1000

    processing_mode = "NORMAL"     # MULTIPROCESSING_POOL | MULTIPROCESSING_PROC | MULTITHREADING | NORMAL

    max_num_tasks = 3  # 3 is the best after tests

    use_betting = True

    win_ratio_final = []

    win_ratio_task = []

    print("Simulating", num_matches, "matches...")

    before_time = time()

    if processing_mode == "NORMAL":
        win_ratio_task = [simulate_matches([num_matches, processing_mode, use_betting])]

        win_ratio_final = win_ratio_task[0]

    elif processing_mode == "MULTIPROCESSING_PROC":
        pass

    elif processing_mode == "MULTIPROCESSING_POOL":

        print_inline("Using multitaks. Calculating...")

        num_matches_task = int(num_matches / max_num_tasks)
        if num_matches_task == 0:
            num_matches_task = 1

        # print(num_matches_task)

        pool = multiprocessing.Pool(processes=max_num_tasks)
        win_ratio_task = pool.map(simulate_matches, [[num_matches_task, processing_mode] for _ in range(0, max_num_tasks)])

        win_ratio_final = tuple(sum(y) / len(y) for y in zip(*win_ratio_task))

        print("")

    elif processing_mode == "MULTITHREADING":
        pass

    after_time = time()

    print("Win Ratio in", num_matches, "games (player x dealer x push): ", win_ratio_final)
    print("Total time: ", after_time - before_time, "seconds")


if __name__ == "__main__":
    Main()

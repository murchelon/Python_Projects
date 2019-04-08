# BlackJack ML 0.1


import random as rnd
import multiprocessing

from time import sleep, time

from bib_support import print_inline, ls, get_card_val
from BlackJack_Alg import blackjack_alg_50X50, blackjack_alg_WIKIPEDIA_BLACKJACK, blackjack_alg_MURCH, blackjack_alg_SIMPLE


class GamePlayer:

    def __init__(self, _name: str, _type: str = "PLAYER", _algoritm: str = "50X50", _cards: list = [], _known_table_cards: list = []):
        self.name = _name
        self.type = _type
        self.cards = _cards
        self.algoritm = _algoritm
        self.known_table_cards = _known_table_cards

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

            # if its the table, the rules says it must hit if has 16 or less
            if self.type == "TABLE":
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


def run_match(deck: list) -> str:

    winner = ""

    player = GamePlayer(_name="Murch", _algoritm="WIKIPEDIA_BLACKJACK", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name="Murch", _algoritm = "MURCH", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name="Murch", _algoritm = "SIMPLE", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck), get_card_from_deck(deck) ])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck, "K"), get_card_from_deck(deck, "8") ])

    table = GamePlayer(_name="Blacu Jacku", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)], _type="TABLE")

    # Table reveals their first card:
    player.known_table_cards = table.cards[0]

    ls("=== MATCH ===========================================")
    ls("Player INIT hand:", player.print_hand(), player.get_card_sum())
    ls("Table  INIT hand:", table.print_hand(), table.get_card_sum())

    ls("-----------------------------------------------------")

    turn = "PLAYER"

    while turn == "PLAYER":

        check_hit = player.should_hit()

        if check_hit == True:
            player.hit(deck)

        ls("PLAYER: check_hit =", check_hit, "| Cartas: ", player.print_hand(), player.get_card_sum())

        if player.get_card_sum() > 21:
            turn = "END"
            winner = "TABLE"
            ls("player exploded!")

        else:
            if check_hit == False:
                turn = "TABLE"

    while turn == "TABLE":

        check_hit = table.should_hit()

        if check_hit == True:
            table.hit(deck)

        ls("TABLE: check_hit =", check_hit, "| Cartas: ", table.print_hand(), table.get_card_sum())

        if table.get_card_sum() > 21:
            turn = "END"
            winner = "PLAYER"
            ls("table exploded!")

        else:
            if check_hit == False:
                turn = "END"

        # ls("-----------------------------------------------------")

    if winner == "":
        if table.get_card_sum() >= player.get_card_sum():
            winner = "TABLE"
        else:
            winner = "PLAYER"

    ls("Player FINAL hand:", player.print_hand(), player.get_card_sum())
    ls("Table  FINAL hand:", table.print_hand(), table.get_card_sum())
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
def simulate_matches(params: list = [1, "NORMAL"]) -> tuple:

    total_win_player = 0
    total_win_table = 0

    number_of_decks = 4

    num_matches = params[0]
    processing_mode = params[1]

    current_deck = new_deck(number_of_decks_used=number_of_decks)  # according to the rules, 8 decks are used

    for x in range(0, num_matches):

        # if there are less then 20 cards in deck, get new decks
        if len(current_deck) <= 20:
            current_deck = new_deck(number_of_decks_used=number_of_decks)

        # print(current_deck)

        # as the rules say, shuffle after every match
        rnd.shuffle(current_deck)

        winner = run_match(current_deck)

        if winner == "PLAYER":
            total_win_player = total_win_player + 1
        else:
            total_win_table = total_win_table + 1

        if x > 9:
            win_ratio_player = (total_win_player * 100) / x
            win_ratio_table = 100 - win_ratio_player

            line = "Real time: Win Ratio in " + str(x + 1) + " games (player x table): " + str(round(win_ratio_player, 5)) + ", " + str(round(win_ratio_table, 5)) + " -- Deck size: " + str(len(current_deck))

            if processing_mode in ["NORMAL"]:
                print_inline(line)

    if num_matches > 10:
        if processing_mode in ["NORMAL"]:
            print("")

    win_ratio_player = (total_win_player * 100) / num_matches
    win_ratio_table = 100 - win_ratio_player

    return win_ratio_player, win_ratio_table


def Main() -> None:
    """
    Main function
    """

    win_ratio_final = []

    win_ratio_task = []

    num_matches = 100000

    processing_mode = "MULTIPROCESSING_POOL"     # MULTIPROCESSING_POOL | MULTIPROCESSING_PROC | MULTITHREADING | NORMAL

    max_num_tasks = 3  # 3 is the best after tests

    print("Simulating", num_matches, "matches...")

    before_time = time()

    if processing_mode == "NORMAL":
        win_ratio_task = [simulate_matches([num_matches, processing_mode])]

        win_ratio_final = win_ratio_task[0]

    elif processing_mode == "MULTIPROCESSING_PROC":
        pass

    elif processing_mode == "MULTIPROCESSING_POOL":

        print_inline("Using multitaks. Calculating...")

        num_matches_task = int(num_matches / max_num_tasks)

        # print(num_matches_task)

        pool = multiprocessing.Pool(processes=max_num_tasks)
        win_ratio_task = pool.map(simulate_matches, [[num_matches_task, processing_mode] for _ in range(0, max_num_tasks)])

        win_ratio_final = tuple(sum(y) / len(y) for y in zip(*win_ratio_task))

        print("")

    elif processing_mode == "MULTITHREADING":
        pass

    after_time = time()

    print("Win Ratio in", num_matches, "games (player x table): ", win_ratio_final)
    print("Total time: ", after_time - before_time, "seconds")


if __name__ == "__main__":
    Main()

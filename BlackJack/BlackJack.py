# BlackJack 0.3
# =============
#
# Blackjack game created to help me learn python.
# The goal is make a program that can play by it's own
# and show the statistics envolved. Expanded to be an real, rich, fast and reliable
# player strategy test ambient
#
# Features:
# =========
#
# - Algoritm that trys to mimic reality the best it cans. The goal is to use ALL rules in BJ and try to create a fast and real envirolment to try differente alooritms to beat the dealer
# - Can use several players with and a dealer
# - hability to use real decks with cards and suits
# - able to use different algoritms to decide if hit ot not
# - Can use as many decks as desired in a given match
# - The decks are consumed by each match and when its near exaustion, the dealer get new decks
# - can look to the cards in the dealer (player "sees" dealer hand)
# - Possible to run hundred of tousands of simulations
# - Multiprocessing, Multithreading (give a number of simulations to a process and create several processes)
# - Set the precision of calculus used and in results
#
# T O D O List:
# =============
#
# - TODO: Implement insurance, the amout payied for insurance, the amout payed by blackjack .. all in parameters
# - DONE -- Fix the order of the dealed cards. They have an order... and it must be followed
# - TODO: make this program be able to play against flash sites with bj games
# - DONE -- Implement spliting of cards
# - DONE -- Implement betting
# - DONE -- Implement push (tie, when neither the player or dealer wins. Today when there is a tie, the dealer wins)
# - DONE -- Implement double
# - DONE -- Implement surrender
# - TODO: Implement algorigm of Machine Learning (this is the main original goal)
# - TODO: Implement algoritm of Card Counting (Hi-Lo ? Must me able to do 2 types of CC: One like the real world and other with simulated real decks "in mind")
# - DONE -- Implement Multithreading to compare performance. Probably worse
# - DONE -- Implement Multiprocessing by NOT using a Pool .. to compare performance
# - TODO: export lots os data and shit to use with Jupyter and Plot and Numpy and etc
# - TODO: Implement game against a human (1 and 2 players ?)
# - TODO: Create a GUI ?
# - DONE -- Find a way to show progress when in multiprocessing mode
# - DONE -- Support more then 1 player (computer dealer x computer x computer...)
# - DONE -- Implement some way of measuring the speed, like 2323 matches / sec
# - DONE -- Implement a real behavior for the dealer. Follow bj rules for dealer
# - TODO: Change several aspects of the program to make it faster. like using sets and many other little changes
# - TODO: Stop using lists ! use NumPY for everything! Performance!
# - TODO: Implement pays more when blackjack (natural)
# - TODO: Add SEVERAL small rules that can be found in https://en.wikipedia.org/wiki/Blackjack
#
#
# - FIX: --  There are sometimes when i try to pop a card from the current deck, but
#            as there are so many players (in games with >30 players) that there is no card to pop
#            need to implement a wat to detect there is no card and create a new current deck. Probably have to make current deck a global var
#
# - FIX: -- When i use 3 players with 1 match... the statistics look wrong. Have to check that
#
# RULES and DETAILS:
# ==================
#
# - Dealer must hit if lower then 16. If ctHIT_ON_SOFT_HAND = True then see comment in the variable
# - Order of play: Dealer gives a card for each player, one for him face up. Then one again for each player and one for him again
# - If using more them one player, the results of them are combined averaged
# - If using more them one task, the results of them are combined averaged
# - The number of decks may be increased in order to accomodade the number of players
# - If the remaining cards in the deck are only ctRESHUFFLE_DECK_PERC (in percentual), then get new shuffled decks up tho the amount of decks defined in the param
# - If player blows, the dealer wins even before he plays (make a huge difference, giving more advantage to the dealer)
# - Can only split once, having 2 game at once
# - Can only split if the FIRST 2 cards are equal. First hand
#
#
# References:
#
# https://pdfs.semanticscholar.org/e1dd/06616e2d18179da7a3643cb3faab95222c8b.pdf
# https://www.888casino.com/blog/blackjack-strategy-guide
# https://www.888casino.com/blog/advantage-play/an-introduction-to-advanced-advantage-play
# https://www.888casino.com/blog/blackjack-tips/why-not-mimic-the-dealer-playing-strategy

import random as rnd
import multiprocessing
import threading

from time import time

from bib_support import print_inline, ls, get_card_val
import BlackJack_Alg as alg
import BlackJack_BetAlg as bet_alg


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
# PARAMETERS
#
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Number of players playing the game against the dealer. Min 1, max > 1  :)
ctNUM_PLAYERS = 1

# Define the strategy algoritm. All players use the same. Dealer uses its won.
# ["NEVER", "ALWAYS", "50X50", "BJ_BASIC_STRAT_FULL", "BJ_BASIC_STRAT_NOSPLIT_NODOUBLE", "MURCH", "DEALER"]
ctSTRAT_ALGORITM = "BJ_BASIC_STRAT_FULL"

# Number of maches being simulated
ctNUM_MATCHES = 10000

# Number of complete decks of cards in play. When there are only 20% of cards in the combined decks, the dealer get a new set of decks and shuffle them
ctNUM_OF_DECKS = 6

# Use betting system. Place bets and try to maximize money. Balance shows in the results
ctUSE_BETTING = True

# Define the betting algoritm. All players use the same. Dealer uses its won.
ctBET_ALGORITM = "DEFAULT"

# Type of processing the matches. Use: NORMAL | MULTIPROCESSING_POOL | MULTIPROCESSING_PROC | MULTITHREADING
ctPROCESSING_MODE = "NORMAL"

# Number os simultaneous processes or threads when using ultitasks. Paralelism. Speeds up the simulation
# in my computer and tests, the fastest value was 2 tasks
ctNUM_SIMULTANEOUS_TASKS = 2

# Precision of the numbers, when returning the statistics. Its rounded to the number of decimals defined here
ctNUM_PRECISION = 6  # arround 46 max

# Dealer must hit on soft 17 (when have an ACE and a 6) ? If not, will hit when sum of cards <= 16, else hit on <= 17 if have an ACE or hit when <= 16 when doesnt have an ACE
ctHIT_ON_SOFT_HAND = False

# Enable the player to split cards when he has a hand that are made of equal cards, on the first hand
ctALLOW_SPLITTING = True

# Enable the player to double the bet in some situations.
ctALLOW_DOUBLE = True

# Enable the player to surrender in some situations.
ctALLOW_SURRENDER = True

# Sets the moment when the deck being used is discarded and the dealer gets new shuffled decks.
# Define the percentual from the decks being used with remaining cards. If its set to 0.2 it means the game will
# get new set of ctNUM_OF_DECKS shuffled to continue the game, when there are 20% of the total number of cards
# that originaly were in the decks
ctRESHUFFLE_DECK_PERC = 0.20


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
# CLASS DEFINITION
#
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class GamePlayer:

    def __init__(self, _ID: int, _name: str, _type: str = "PLAYER", _algoritm: str = "50X50", _cards: list = [], _known_dealer_cards: list = [], _start_money: float = 1000.0, _betting_algoritm: str = "DEFAULT"):
        self.ID = _ID
        self.name = _name
        self.type = _type
        self.cards = _cards

        if _type == "DEALER":
            self.algoritm = "DEALER"
            self.betting_algoritm = ""
        else:
            self.algoritm = _algoritm.upper()
            self.betting_algoritm = _betting_algoritm

        self.known_dealer_cards = _known_dealer_cards

        self.start_money = _start_money
        self.final_money = _start_money
        self.actual_bet = 0

        self.cards_splitted = []
        self.actual_bet_splitted = 0

        self.last_action = ""
        self.winning_state = ""

    def hit(self, _deck_used: list, _card: list = [], _hand_number: int = 0) -> None:

        if _card == []:
            if _hand_number == 0:
                self.cards.append(get_card_from_deck(_deck_used))
            else:
                self.cards_splitted.append(get_card_from_deck(_deck_used))

        else:
            if _hand_number == 0:
                self.cards.append(_card)
            else:
                self.cards_splitted.append(_card)

    def print_hand(self, _hand_number: int = 0) -> list:

        # return [ x[0] + "|" + x[1] + "|" + str(get_card_val(x[0])) for x in self.cards ]
        # return [ x[0] + "|" + x[1] for x in self.cards ]
        # return [ x[0] + " " + str(get_card_val(x[0])) +  x[1] for x in self.cards ]

        if ctALLOW_SPLITTING:
            if _hand_number == 0:
                cards = self.cards
            else:
                cards = self.cards_splitted
        else:
            cards = self.cards

        return [x[0] + x[1] for x in cards]

    def get_card_sum(self, _hand_number: int = 0) -> int:

        sum_ = 0

        if ctALLOW_SPLITTING:
            if _hand_number == 0:
                cards = self.cards
            else:
                cards = self.cards_splitted
        else:
            cards = self.cards

        num_of_aces = len([x[0] for x in cards if x[0] == "A"])

        if num_of_aces == 0:

            for card in cards:

                sum_ += get_card_val(card[0])

        elif num_of_aces == 1:

            for card in cards:

                # test with A = 11
                if get_card_val(card[0]) == 1:
                    sum_ += 11
                else:
                    sum_ += get_card_val(card[0])

            # if too big value
            if sum_ > 21:

                # uses 1 for the A
                sum_ = 0

                for card in cards:
                    sum_ += get_card_val(card[0])

        elif num_of_aces >= 2:

            val_for_aces = 12

            # test with both aces value = 12 (11 + 1)
            for card in cards:

                if get_card_val(card[0]) != 1:
                    sum_ += get_card_val(card[0])

            sum_ = sum_ + val_for_aces

            # if too big value
            if sum_ > 21:

                # uses both aces value = 2 (1 + 1)
                sum_ = 0
                val_for_aces = 2

                for card in cards:

                    if get_card_val(card[0]) != 1:
                        sum_ += get_card_val(card[0])

                sum_ = sum_ + val_for_aces

        return sum_

    def get_next_action(self, _force: str = None, _hand_number: int = 0) -> str:

        ret = ""

        if _force is None:

            # test if the selected alg is implemented
            if self.algoritm not in alg.AVALIABLE_ALGS:
                raise ValueError("The selected algoritm is not implemented. Selected: " + self.algoritm + " | Avaliable: " + str(avaliable_algs))

            # check witch alg to use and use it
            if self.algoritm == "DEALER":
                ret = alg.blackjack_alg_DEALER(self, ctHIT_ON_SOFT_HAND)

            elif self.algoritm == "50X50":
                ret = alg.blackjack_alg_50X50()

            elif self.algoritm == "BJ_BASIC_STRAT_FULL":

                ret = alg.blackjack_alg_BJ_BASIC_STRAT_FULL(self, _hand_number, ctHIT_ON_SOFT_HAND, ctALLOW_SPLITTING, ctALLOW_DOUBLE, ctALLOW_SURRENDER)

            elif self.algoritm == "BJ_BASIC_STRAT_NOSPLIT_NODOUBLE":
                ret = alg.blackjack_alg_BJ_BASIC_STRAT_NOSPLIT_NODOUBLE(self)

            elif self.algoritm == "MURCH":
                ret = alg.blackjack_alg_MURCH(self)

            elif self.algoritm == "SIMPLE":
                ret = alg.blackjack_alg_SIMPLE(self)

            # if has 21 or more, always say no to hit
            if self.get_card_sum(_hand_number=_hand_number) >= 21:
                ret = "STAND"

             # hard coded always and never, for tests. Last test so it prevales from any other test
            if self.algoritm == "NEVER":
                ret = "STAND"

            elif self.algoritm == "ALWAYS":
                ret = "HIT"

            if ret == "":

                if _hand_number == 0:
                    cards = caller.cards
                    print("ERROR: get_next_action returned no action. _hand_number = " + str(_hand_number) + " | Player cards: " + cards)

                else:
                    cards = caller.cards_splitted
                    print("ERROR: get_next_action returned no action. _hand_number = " + str(_hand_number) + " | Player cards_splitted: " + cards)

            self.last_action = ret

            return ret

        else:

            self.last_action = _force

            return _force

    def define_bet_value(self, _force: float = None) -> float:

        ret = False

        avaliable_algs = ["DEFAULT"]

        if _force is None:

            # test if the selected alg is implemented
            if self.betting_algoritm not in avaliable_algs:
                raise ValueError("The selected betting algoritm is not implemented. Selected: " + self.algoritm + " | Avaliable: " + str(avaliable_algs))

            # check witch alg to use and use it
            if self.betting_algoritm == "DEFAULT":
                ret = bet_alg.blackjack_alg_BET_DEFAUT(self, ctHIT_ON_SOFT_HAND)

            return ret

        else:
            return _force

    def can_split(self) -> bool:
        # dont check if ctALLOW_SPLITTING = true because this function wants to return only the information
        # about being able to split or not. It doesnt matter if its activated or not

        # if player has only 2 cards
        if len(self.cards) == 2:

            # if player is not already splitted
            if self.cards_splitted == []:

                # if the player really have 2 equal cards. J, Q and K are treated the same. 10 are not equal J,Q or K
                if self.cards[0][0] == self.cards[1][0]:
                    return True

                elif (self.cards[0][0] in ["J", "Q", "K"]) and (self.cards[1][0] in ["J", "Q", "K"]):
                    return True

        return False

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def Main() -> None:

    print("Simulating", ctNUM_MATCHES, "match ..." if ctNUM_MATCHES == 1 else "matches ...")

    before_time = time()
    speed = 0

    run_simulation_project(ctNUM_MATCHES, ctPROCESSING_MODE, ctNUM_PLAYERS)

    passed_time = time() - before_time

    if passed_time > 0:
        speed = ctNUM_MATCHES / passed_time

    print("Total time: ", round(passed_time, 2), "seconds -- " + str(round(speed, 2)) + " matches/s")


def run_simulation_project(num_matches: int = 1, processing_mode: str = "NORMAL", num_players: int = 1) -> None:
    """
    Main function to be called. Runs the entire simulation with the desired parameters
    """

    win_ratio_final = []

    win_ratio_helper = []

    win_ratio_simu = []

    num_matches_task = int(num_matches / (ctNUM_SIMULTANEOUS_TASKS))
    if num_matches_task == 0:
        num_matches_task = 1

    if processing_mode == "NORMAL":

        win_ratio_simu = [simulate_matches([num_matches, processing_mode, num_players])]

        # print (win_ratio_simu[0])

        win_ratio_final = tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*win_ratio_simu[0]))

        # win_ratio_final = win_ratio_simu[0]

    elif processing_mode == "MULTIPROCESSING_PROC":

        print_inline("Using multitaks. Calculating...")

        print("")

        jobs = []

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []

        for i in range(ctNUM_SIMULTANEOUS_TASKS):
            p = multiprocessing.Process(target=simulate_matches, args=([num_matches_task, processing_mode, num_players], i, return_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        # print (return_dict.values())

        for proc_num in return_dict.values():

            win_ratio_helper.append(tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*proc_num)))

        win_ratio_final = tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*win_ratio_helper))

        print("")

    elif processing_mode == "MULTIPROCESSING_POOL":

        print_inline("Using multitaks. Calculating...")

        print("")

        # print(num_matches_task)

        pool = multiprocessing.Pool(processes=ctNUM_SIMULTANEOUS_TASKS)
        win_ratio_simu = pool.map(simulate_matches, [[num_matches_task, processing_mode, num_players] for _ in range(0, ctNUM_SIMULTANEOUS_TASKS)])

        # print("win_ratio_simu = " + str(win_ratio_simu))

        for proc_num in win_ratio_simu:

            win_ratio_helper.append(tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*proc_num)))

            # print("proc_num1 = " + str(proc_num))
            # print("win_ratio_helper = " + str(win_ratio_helper))

        win_ratio_final = tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*win_ratio_helper))

        # print("final = " + str(win_ratio_final))

        print("")

    elif processing_mode == "MULTITHREADING":

        print_inline("Using multitaks. Calculating...")

        print("")

        jobs = []

        for proc in jobs:
            proc.join()

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        for i in range(ctNUM_SIMULTANEOUS_TASKS):
            t = threading.Thread(target=simulate_matches, args=([num_matches_task, processing_mode, num_players], i, return_dict))
            t.daemon = True
            jobs.append(t)
            t.start()

        for proc in jobs:
            proc.join()

        # print (return_dict.values())

        for proc_num in return_dict.values():

            win_ratio_helper.append(tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*proc_num)))

            # print("proc_num1 = " + str(proc_num))
            # print("win_ratio_helper = " + str(win_ratio_helper))

        win_ratio_final = tuple(round(sum(y) / len(y), ctNUM_PRECISION) for y in zip(*win_ratio_helper))

        # print("final = " + str(win_ratio_final))

        print("")

    mask = "{:." + str(ctNUM_PRECISION) + "f}"
    # mask.format(win_ratio_final[0])

    if ctALLOW_SURRENDER:
        formated_result = mask.format(win_ratio_final[0]), mask.format(win_ratio_final[1]), mask.format(win_ratio_final[2]), mask.format(win_ratio_final[3])
        print("FINAL TOTAL Win Ratio in", ctNUM_MATCHES, "game(s) (player x dealer x push x surrender): ", formated_result)
    else:

        formated_result = mask.format(win_ratio_final[0]), mask.format(win_ratio_final[1]), mask.format(win_ratio_final[2])

        print("FINAL TOTAL Win Ratio in", ctNUM_MATCHES, "game(s) (player x dealer x push): ", formated_result)


def simulate_matches(params: list, index_proc: int = -1, return_dict: list = None) -> list:
    """
    runs the entire desired number of matches
    """

    global ctNUM_OF_DECKS

    aGamePlayers = []

    speed = 0

    # internal params. values from arguments
    num_matches = params[0]
    processing_mode = params[1]
    num_players = params[2]

    total_win_player = [0 for _ in range(0, num_players)]
    total_win_dealer = [0 for _ in range(0, num_players)]
    total_win_push = [0 for _ in range(0, num_players)]
    total_win_surrender = [0 for _ in range(0, num_players)]

    # if the number of players (plus dealer) times 9 cards each is more then the avaliable cards, incrise deck number to support the game
    if (num_players + 1) * 9 >= ctNUM_OF_DECKS * 54:
        ctNUM_OF_DECKS = int((num_players + 1) * 6) + 1
        print("To many players. Increasing deck numeber to " + str(ctNUM_OF_DECKS))

    current_deck = new_deck(number_of_decks_used=ctNUM_OF_DECKS)

    # dealer = GamePlayer(0, _name="Blacu Jacku Dueler", _algoritm="DEALER", _type="DEALER", _cards=[])
    # player = GamePlayer(1, _name="Murch", _algoritm="BJ_BASIC_STRAT", _cards=[])

    # add dealer
    aGamePlayers.append(GamePlayer(0, _name="Blacu Jacku Dueler", _algoritm="DEALER", _type="DEALER", _cards=[]))

    for conta_player in range(1, num_players + 1):
        aGamePlayers.append(GamePlayer(conta_player, _name="Player " + str(conta_player), _algoritm=ctSTRAT_ALGORITM, _cards=[], _betting_algoritm=ctBET_ALGORITM))

    before_time = time()

    params_used = str(num_players) + " player(s), 1 Dealer, " + str(ctNUM_OF_DECKS) + " decks, Use betting: " + str(ctUSE_BETTING) + ", Betting Alg: " + ctBET_ALGORITM + ", Strategy Alg: " + ctSTRAT_ALGORITM + ", Processing mode: " + processing_mode

    if processing_mode != "NORMAL":
        params_used = params_used + " (Tasks: " + str(ctNUM_SIMULTANEOUS_TASKS) + ")"

    print(params_used)

    # keeps track of how many splits occoured so we can updare statistis
    split_count = 0

    for x in range(0, num_matches):

        # if there are less then 20 cards in deck, get new decks
        if len(current_deck) <= int(ctNUM_OF_DECKS * 52 * ctRESHUFFLE_DECK_PERC):
            current_deck = new_deck(number_of_decks_used=ctNUM_OF_DECKS)

        # print(current_deck)

        winner = run_match(current_deck, aGamePlayers)

        for conta_player in range(0, len(winner)):

            if winner[conta_player] == "PLAYER":
                total_win_player[conta_player] = total_win_player[conta_player] + 1

            elif winner[conta_player] == "DEALER":
                total_win_dealer[conta_player] = total_win_dealer[conta_player] + 1

            elif winner[conta_player] == "PUSH":
                total_win_push[conta_player] = total_win_push[conta_player] + 1

            elif winner[conta_player] == "SURRENDER":
                total_win_surrender[conta_player] = total_win_surrender[conta_player] + 1

            # search for the | indicating that it was a splitted hand and have 2 possible values for winnings
            elif winner[conta_player].find("|") > 0:

                split_count = split_count + 1

                _local_wins = []
                _win_count = 0

                for win in winner[conta_player].split("|"):

                    if win == "PLAYER":
                        total_win_player[conta_player] = total_win_player[conta_player] + 1

                    elif win == "DEALER":
                        total_win_dealer[conta_player] = total_win_dealer[conta_player] + 1

                    elif win == "PUSH":
                        total_win_push[conta_player] = total_win_push[conta_player] + 1

                    elif win == "SURRENDER":
                        total_win_surrender[conta_player] = total_win_surrender[conta_player] + 1

                    _win_count = _win_count + 1

        _helper = x
        if _helper + split_count == 0:
            _helper = 1

        win_ratio_player = (total_win_player[0] * 100) / (_helper + split_count)
        win_ratio_dealer = (total_win_dealer[0] * 100) / (_helper + split_count)
        win_ratio_push = (total_win_push[0] * 100) / (_helper + split_count)
        win_ratio_surrender = (total_win_surrender[0] * 100) / (_helper + split_count)

        passed_time = time() - before_time

        if passed_time > 0:
            speed = x / (passed_time)
        # check_sum = win_ratio_player + win_ratio_dealer + win_ratio_push

        if ctALLOW_SURRENDER:

            line = "Proc1, Player1, Match: " + "{:06d}".format(x + 1) + " (player x dealer x push x surrender): " \
                + "{:.8f}".format(win_ratio_player) + ", " \
                + "{:.8f}".format(win_ratio_dealer) + ", " \
                + "{:.8f}".format(win_ratio_push) + ", " \
                + "{:.8f}".format(win_ratio_surrender)

        else:

            line = "Proc1, Player1, Match: " + "{:06d}".format(x + 1) + " (player x dealer x push): " \
                + "{:.8f}".format(win_ratio_player) + ", " \
                + "{:.8f}".format(win_ratio_dealer) + ", " \
                + "{:.8f}".format(win_ratio_push)

        if ctUSE_BETTING:
            line += " -- P1$: {:.2f}".format(aGamePlayers[1].final_money) + " x {:.2f}".format(aGamePlayers[0].final_money) + " :D$"

        if ctALLOW_SPLITTING:
            line += " -- " + str(split_count) + " splits"

        line += " -- {:.2f}".format(speed) + " matches/s"

        if index_proc in [-1, 0] or processing_mode == "NORMAL":
            print_inline(line)

    if num_matches > 10:
        if processing_mode in ["NORMAL"]:
            print("")

    final_result = []

    for conta_player in range(0, num_players):

        win_ratio_player = (total_win_player[conta_player] * 100) / (num_matches + split_count)
        win_ratio_dealer = (total_win_dealer[conta_player] * 100) / (num_matches + split_count)
        win_ratio_push = (total_win_push[conta_player] * 100) / (num_matches + split_count)
        win_ratio_surrender = (total_win_surrender[conta_player] * 100) / (num_matches + split_count)

        final_result.append((round(win_ratio_player, ctNUM_PRECISION), round(win_ratio_dealer, ctNUM_PRECISION), round(win_ratio_push, ctNUM_PRECISION), round(win_ratio_surrender, ctNUM_PRECISION)))

    if return_dict is not None:
        return_dict[index_proc] = final_result

    if ctUSE_BETTING:
        print("")
        print("BALANCE:")

        reminder = 0

        for conta_player in range(0, num_players + 1):

            if conta_player == 0:

                print("Start: " + str("{:.2f}".format(round(aGamePlayers[conta_player].start_money, 2))) + " | End: " + str("{:.2f}".format(round(aGamePlayers[conta_player].final_money, 2))) + "   -- " + aGamePlayers[conta_player].name)

            else:

                if num_players > 0:

                    reminder += round(aGamePlayers[conta_player].final_money, 2)

                    print("Start: " + str("{:.2f}".format(round(aGamePlayers[conta_player].start_money, 2))) + " | End: " + str("{:.2f}".format(round(aGamePlayers[conta_player].final_money, 2))) + "   -- " + aGamePlayers[conta_player].name)

                else:

                    reminder = (round(aGamePlayers[0].final_money, 2) + round(aGamePlayers[conta_player].final_money, 2)) - (aGamePlayers[0].start_money + aGamePlayers[conta_player].start_money)

                    print("Start: " + str("{:.2f}".format(round(aGamePlayers[conta_player].start_money, 2))) + " | End: " + str("{:.2f}".format(round(aGamePlayers[conta_player].final_money, 2))) + " | rem = " + str(reminder) + "   -- " + aGamePlayers[conta_player].name)

        if num_players > 0:

            reminder = reminder + round(aGamePlayers[0].final_money, 2)

            for conta_player in range(0, num_players + 1):

                reminder = reminder - round(aGamePlayers[conta_player].start_money, 2)

            print("Final reminder = " + str(reminder))

        print("")

    return final_result


def run_match(deck: list, arrGamePlayers: object) -> list:
    """
    runs one match between a dealer and players, using the deck in place at the moment
    returns a list with the result in N positions, 1 for each player, in order (player1, player2, etc)
    Ex.: 3 players. REsult: ["PLAYER", "PLAYER", "DEALER"] . In this result the player 1 and 2 won.. while the 
    player 3 lost.winner
    Here is where all the blackjack rules should be used and applyed
    When splitting is allowed, results will be like: ["PLAYER", "PLAYER|DEALER", "DEALER"] 
    In this result the player 1 won, player2 splitted and won 1 hand and lost the other and the 3rd
    player also lost (and didnt split, as the 1st player also didnt split)
    """

    winner = []
    ret_result = []

    #  create player and dealer
    # dealer = GamePlayer(0, _name="Blacu Jacku Dueler", _algoritm="DEALER", _type="DEALER", _cards=[])
    # player = GamePlayer(1, _name="Murch", _algoritm="BJ_BASIC_STRAT", _cards=[])

    # clean the hand and betting for the next match
    for player in arrGamePlayers:

        player.known_dealer_cards = []
        player.cards = []
        player.cards_splitted = []

        player.last_action = ""
        player.winning_state = ""

        if ctUSE_BETTING is True:
            player.actual_bet = 0
            player.actual_bet_splitted = 0

    # if we are using bets, then, place bet
    if ctUSE_BETTING is True:

        for player in arrGamePlayers:
            if player.type != "DEALER":

                # define the players bet based in the selected algoritm
                player.actual_bet = player.define_bet_value()

                # subtract the bet from player, when starting game
                player.final_money = player.final_money - player.actual_bet

    # Players get 1 card
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.hit(deck)

    # Dealer get 1 card face up
    for dealer in arrGamePlayers:
        if dealer.type == "DEALER":
            dealer.hit(deck)

    # dealer reveals their first card to players
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.known_dealer_cards = arrGamePlayers[0].cards[0]

    # Players get 1 more card
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.hit(deck)

    # Dealer get 1 more card face down
    for dealer in arrGamePlayers:
        if dealer.type == "DEALER":
            dealer.hit(deck)

    # player = GamePlayer(_name="Murch", _algoritm = "MURCH", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name="Murch", _algoritm = "SIMPLE", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck), get_card_from_deck(deck) ])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck, "K"), get_card_from_deck(deck, "8") ])

    # For tests using exacr situations (the exact cards you want), use the arrays bellow:
    # arrGamePlayers[0].cards = [['7', '♣'], ['6', '♦'], ['8', '♣']]
    # arrGamePlayers[1].cards = [['7', '♠'], ['10', '♥']]
    # arrGamePlayers[1].cards_splitted = [['7', '♣'], ['6', '♣'], ['10', '♥']]
    # arrGamePlayers[1].known_dealer_cards = ['7', '♣']

    # arrGamePlayers[0].cards = [['K', '♣'], ['K', '♠']]
    # arrGamePlayers[1].cards = [['8', '♠'], ['A', '♠']]
    # arrGamePlayers[2].cards = [['A', '♠'], ['J', '♥']]

    turn = "PLAYERS"

    while turn == "PLAYERS":

        for player in list(arrGamePlayers):

            if player.type != "DEALER":

                # player_done is a list with 2 positions. The first is the first hand that all players have
                # the second is the splitted hand, that becames false when a player splits
                player_done = False

                # total_hands_number: is the var that controls with hand, in case of splitted cards, are we dealing with
                # it can go from 0 to N, being the number of the hand
                # Today it only supports 1 normal hand and 1 other that is the split.
                # In this case, the normal hand is total_hands_number = 0 and the splitted total_hands_number = 1
                # in the future i plan to allow more splitted hands, the total_hands_number would be 2, 3, etc
                # every player has at least 1 hand ... so the total_hands_number = 0 initialy for them
                total_hands_number = 0
                hand = 0
                splited_results = []
                goto_next_hand = False

                # check if is splitted and adjusts total_hands_number accordingly
                if player.cards_splitted != []:
                    total_hands_number = 1

                while player_done is False:

                    check_hit = player.get_next_action(_hand_number=hand)

                    if check_hit == "HIT":

                        player.hit(_deck_used=deck, _hand_number=hand)

                    elif check_hit == "SPLIT":

                        if ctALLOW_SPLITTING:

                            if player.can_split():

                                total_hands_number = 1

                                # splits the hand
                                player.cards_splitted = [player.cards[1]]
                                player.cards = [player.cards[0]]

                                # give 1 new card for each hand
                                player.hit(deck)
                                player.hit(_deck_used=deck, _hand_number=1)

                                if ctUSE_BETTING is True:

                                    # subtracts another bet from player
                                    player.final_money = player.final_money - player.actual_bet

                                    # put the same bet value in the new splitted cards
                                    player.actual_bet_splitted = player.actual_bet

                                    # debug do erro split nasty
                                    # if 1==1:
                                    #     pass
                            else:
                                player.hit(_deck_used=deck, _hand_number=hand)

                        else:
                            player.hit(deck)

                    elif check_hit == "DOUBLE":

                        if ctUSE_BETTING is True:

                            if hand == 0:
                                player.final_money = player.final_money - player.actual_bet
                                player.actual_bet = player.actual_bet * 2

                            else:
                                player.final_money = player.final_money - player.actual_bet_splitted
                                player.actual_bet_splitted = player.actual_bet_splitted * 2

                            player.hit(_deck_used=deck, _hand_number=hand)

                            if total_hands_number > 0:
                                goto_next_hand = True
                            else:
                                player_done = True
                        else:

                            player.hit(_deck_used=deck, _hand_number=hand)

                    elif check_hit == "SURRENDER":

                        if ctALLOW_SURRENDER:

                            if hand == 0:
                                if total_hands_number > 0:
                                    goto_next_hand = True
                                else:
                                    player_done = True

                            else:
                                player_done = True

                        else:
                            player.hit(_deck_used=deck, _hand_number=hand)

                    elif check_hit == "STAND":

                        if hand == 0:
                            if total_hands_number > 0:
                                goto_next_hand = True
                            else:
                                player_done = True

                        else:
                            player_done = True

                    if player.get_card_sum(_hand_number=hand) > 21:

                        if total_hands_number > 0:

                            splited_results.append("DEALER")

                            if hand == 0:
                                goto_next_hand == True
                                player.winning_state = "DEALER|"
                            else:
                                player_done = True
                                player.winning_state += "DEALER"

                        else:
                            winner.append("DEALER")

                            player.winning_state = "DEALER"

                            player_done = True

                    else:

                        if check_hit == "STAND" or check_hit == "DOUBLE":

                            if total_hands_number > 0:

                                splited_results.append("STAND")

                                if hand == 0:
                                    goto_next_hand == True
                                    player.winning_state = "STAND|"
                                else:
                                    player_done = True
                                    player.winning_state += "STAND"

                            else:
                                winner.append("STAND")
                                player.winning_state = "STAND"
                                player_done = True

                        if check_hit == "SURRENDER":

                            if total_hands_number > 0:

                                splited_results.append("SURRENDER")

                                if hand == 0:
                                    goto_next_hand == True
                                    player.winning_state = "SURRENDER|"
                                else:
                                    player_done = True
                                    player.winning_state += "SURRENDER"

                            else:
                                winner.append("SURRENDER")
                                player.winning_state = "SURRENDER"
                                player_done = True

                    if goto_next_hand == True:

                        hand = 1
                        goto_next_hand = False

                if total_hands_number > 0:

                    winner.append(splited_results[0] + "|" + splited_results[1])

        turn = "DEALER"

    while turn == "DEALER":

        for dealer in arrGamePlayers:
            if dealer.type == "DEALER":

                dealer_done = False

                while dealer_done is False:

                    check_hit = dealer.get_next_action()

                    if check_hit == "HIT":
                        dealer.hit(deck)
                    else:
                        dealer_done = True

                    if dealer.get_card_sum() > 21:

                        # insert the result of the dealer in the 1st position of the result list
                        winner.insert(0, "BLOW")
                        dealer.winning_state = "BLOW"

                        dealer_done = True

                        ls(dealer.name, "exploded!")

                    else:
                        if dealer_done == True:
                            # insert the result of the dealer in the 1st position of the result list
                            winner.insert(0, "STAND")
                            dealer.winning_state = "STAND"

                    ls(dealer.name, ": check_hit =", check_hit, "| Cartas: ", dealer.print_hand(), dealer.get_card_sum())

        turn = "END"

    dealer_sum = 0
    player_sum = 0

    # debug do nasty split
    # if len(winner) <= 2:
    #     # pass
    #     print("teste")

    # check if dealer exploded. All players that are not exploded wins
    # Dealer is always the first position of the winner list
    if winner[0] == "BLOW":

        for x in range(0, len(winner)):
            if x > 0:
                if winner[x] == "STAND":

                    winner[x] = "PLAYER"
                    arrGamePlayers[x].winning_state = "PLAYER"

                    if ctUSE_BETTING is True:

                        # subtracts the dealer
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet

                        # pays the player. times 1 because we return the bet and pay the bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet * 2)

                elif winner[x] == "DEALER":

                    arrGamePlayers[0].winning_state = "DEALER"

                    if ctUSE_BETTING is True:

                        # murch aqui nao e
                        # adds to the dealer
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet

                        # dont do anything to the player because he has already gave money when placing bet and recieving cards
                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                elif winner[x] == "SURRENDER":

                    arrGamePlayers[x].winning_state = "SURRENDER"

                    if ctUSE_BETTING is True:
                        # add to the dealer
                        # murch aqui nao e
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet / 2)

                        # player looses half of the bet only, so return half of his bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet / 2)

                # search for the | indicating that it was a splitted hand and have 2 possible values for winnings
                elif winner[x].find("|") > 0:

                    _local_wins = []
                    _win_count = 0

                    for win in winner[x].split("|"):

                        if win == "STAND" or win == "PLAYER":

                            _local_wins.append("PLAYER")

                            if _win_count == 0:
                                arrGamePlayers[x].winning_state = "PLAYER"
                            elif _win_count == 1:
                                arrGamePlayers[x].winning_state = "|PLAYER"

                            if ctUSE_BETTING is True:

                                if _win_count == 0:

                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet * 2)

                                elif _win_count == 1:
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet_splitted
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet_splitted * 2)

                        elif win == "DEALER":

                            _local_wins.append("DEALER")

                            if _win_count == 0:
                                arrGamePlayers[x].winning_state = "DEALER"
                            elif _win_count == 1:
                                arrGamePlayers[x].winning_state = "|DEALER"

                            if ctUSE_BETTING is True:

                                if _win_count == 0:
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                                    # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                                elif _win_count == 1:
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet_splitted
                                    # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet_splitted

                        elif win == "SURRENDER":

                            _local_wins.append("SURRENDER")

                            if _win_count == 0:
                                arrGamePlayers[x].winning_state = "SURRENDER"
                            elif _win_count == 1:
                                arrGamePlayers[x].winning_state = "|SURRENDER"

                            if ctUSE_BETTING is True:

                                if _win_count == 0:
                                    # murch aqui nao e
                                    # add to the dealer
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet / 2)

                                    # player looses half of the bet only, so return half of his bet
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet / 2)

                                elif _win_count == 1:

                                    # murch aqui nao e

                                    # add to the dealer
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet_splitted / 2)

                                    # player looses half of the bet only, so return half of his bet
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet_splitted / 2)

                        _win_count = _win_count + 1

                    # updates the winner with the correct results
                    winner[x] = _local_wins[0] + "|" + _local_wins[1]

    else:

        for x in range(0, len(winner)):

            if x == 0:

                dealer_sum = arrGamePlayers[x].get_card_sum()

            else:

                if winner[x] == "STAND":

                    player_sum = arrGamePlayers[x].get_card_sum()

                    if dealer_sum == player_sum:

                        winner[x] = "PUSH"

                        arrGamePlayers[x].winning_state = "PUSH"

                        if ctUSE_BETTING is True:
                            # arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                            arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet

                    elif dealer_sum > player_sum:

                        winner[x] = "DEALER"

                        arrGamePlayers[x].winning_state = "DEALER"

                        if ctUSE_BETTING is True:
                            arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                            # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                    elif dealer_sum < player_sum:

                        winner[x] = "PLAYER"

                        arrGamePlayers[x].winning_state = "PLAYER"

                        if ctUSE_BETTING is True:
                            arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet
                            arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet * 2)

                elif winner[x] == "DEALER":

                    # murch pode ser aqui
                    player_sum = arrGamePlayers[x].get_card_sum()

                    arrGamePlayers[x].winning_state = "DEALER"

                    if ctUSE_BETTING is True:
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                elif winner[x] == "SURRENDER":

                    arrGamePlayers[x].winning_state = "SURRENDER"

                    if ctUSE_BETTING is True:
                        # add to the dealer
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet / 2)

                        # player looses half of the bet only, so return half of his bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet / 2)

                # search for the | indicating that it was a splitted hand and have 2 possible values for winnings
                elif winner[x].find("|") > 0:

                    _local_wins = []
                    _win_count = 0

                    for win in winner[x].split("|"):

                        if win == "STAND":

                            player_sum = arrGamePlayers[x].get_card_sum(_hand_number=_win_count)

                            if dealer_sum == player_sum:

                                _local_wins.append("PUSH")

                                if _win_count == 0:
                                    arrGamePlayers[x].winning_state = "PUSH"
                                elif _win_count == 1:
                                    arrGamePlayers[x].winning_state = "|PUSH"

                                if ctUSE_BETTING is True:
                                    # arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                                    # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet

                                    if _win_count == 0:
                                        #  murch aqui nao e
                                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet
                                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                                    elif _win_count == 1:
                                        #  murch aqui nao e
                                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet_splitted
                                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet_splitted

                            elif dealer_sum > player_sum:

                                _local_wins.append("DEALER")

                                if _win_count == 0:
                                    arrGamePlayers[x].winning_state = "DEALER"
                                elif _win_count == 1:
                                    arrGamePlayers[x].winning_state = "|DEALER"

                                if ctUSE_BETTING is True:

                                    if _win_count == 0:

                                        # murch aqui nao e
                                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                                    elif _win_count == 1:
                                        # murch aqui nao e
                                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet_splitted
                                        # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet_splitted

                            elif dealer_sum < player_sum:

                                _local_wins.append("PLAYER")

                                if _win_count == 0:
                                    arrGamePlayers[x].winning_state = "PLAYER"
                                elif _win_count == 1:
                                    arrGamePlayers[x].winning_state = "|PLAYER"

                                if ctUSE_BETTING is True:

                                    if _win_count == 0:
                                        # murch aqui nao e
                                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet
                                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet * 2)

                                    elif _win_count == 1:
                                        # murch aqui nao e
                                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet_splitted
                                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + (arrGamePlayers[x].actual_bet_splitted * 2)

                        elif win == "DEALER":

                            _local_wins.append("DEALER")

                            if _win_count == 0:
                                arrGamePlayers[x].winning_state = "DEALER"
                            elif _win_count == 1:
                                arrGamePlayers[x].winning_state = "|DEALER"

                            if ctUSE_BETTING is True:

                                if _win_count == 0:
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                                    # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                                elif _win_count == 1:
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet_splitted
                                    # arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet_splitted

                        elif win == "SURRENDER":

                            _local_wins.append("SURRENDER")

                            if _win_count == 0:
                                arrGamePlayers[x].winning_state = "SURRENDER"
                            elif _win_count == 1:
                                arrGamePlayers[x].winning_state = "|SURRENDER"

                            if ctUSE_BETTING is True:

                                if _win_count == 0:
                                    # add to the dealer
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet / 2)

                                    # player looses half of the bet only, so return half of his bet
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet / 2)

                                elif _win_count == 1:

                                    # add to the dealer
                                    # murch aqui nao e
                                    arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + int(arrGamePlayers[x].actual_bet_splitted / 2)

                                    # player looses half of the bet only, so return half of his bet
                                    arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + int(arrGamePlayers[x].actual_bet_splitted / 2)

                        _win_count = _win_count + 1

                    # updates the winner with the correct results
                    # winner[x] = "|".join(_local_wins)
                    # murch aqui nao e
                    winner[x] = _local_wins[0] + "|" + _local_wins[1]

    ls("Player FINAL hand:", player.print_hand(), player.get_card_sum())
    ls("dealer  FINAL hand:", dealer.print_hand(), dealer.get_card_sum())
    ls("WINNER:", winner)

    ls("=== FINAL ===========================================")

    ls("\n\n")

    return winner[1:]


def new_deck(shuffled: bool = True, number_of_decks_used: int = 1) -> list:
    """
    return a number of new decks, complete, shuffled or not, as a list
    """

    values = [str(x) for x in range(2, 11)] + ["J", "Q", "K", "A"]

    suits = ["♦", "♠", "♥", "♣"]  # ♥♦♣♠

    deck_final = []

    for x in range(1, number_of_decks_used + 1):
        deck = [[value, suit] for value in values for suit in suits]

        deck_final = deck_final + deck

    if shuffled == True:
        rnd.shuffle(deck_final)

    return deck_final


def get_card_from_deck(deck: list, forceValue: str = None) -> list:
    """
    hummm ... get a new card from the deck ?
    """
    # if deck == []:
    #     current_deck = new_deck(number_of_decks_used=ctNUM_OF_DECKS)

    if forceValue is None:
        return deck.pop()
    else:
        return [forceValue, "♥"]


if __name__ == "__main__":

    Main()

# BlackJack 0.3
# =============
#
# Blackjack game created to help me learn python.
# The goal is make a program that can play by it's own
# and show the statistics envolved.
#
# Features:
# =========
#
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
# - TODO: Implement double down, surrender, insurance, the amout payied for insurance, the amout payed by blackjack .. all in parameters
# - DONE -- Fix the order of the dealed cards. They have an order... and it must be followed
# - TODO: make this program be able to play against flash sites with bj games
# - TODO: Implement spliting of cards
# - TODO: Implement betting
# - DONE -- Implement push (tie, when neither the player or dealer wins. Today when there is a tie, the dealer wins)
# - TODO: Implement algorigm of Machine Learning (this is the main original goal)
# - TODO: Implement algoritm of Card Counting (Hi-Lo ? Must me able to do 2 types of CC: One like the real world and other with simulated real decks "in mind")
# - DONE -- Implement Multithreading to compare performance. Probably worse
# - DONE -- Implement Multiprocessing by NOT using a Pool .. to compare performance
# - TODO: export lots os data and shit to use with Jupyter and Plot and Numpy and etc
# - TODO: Implement game against a human (1 and 2 players ?)
# - TODO: Create a GUI ?
# - TODO: Find a way to show progress when in multiprocessing mode
# - DONE -- Support more then 1 player (computer dealer x computer x computer...)
# - DONE -- Implement some way of measuring the speed, like 2323 matches / sec
# - DONE -- Implement a real behavior for the dealer. Follow bj rules for dealer
# - TODO: Change several aspects of the program to make it faster. like using sets and many other little changes
# - TODO: Stop using lists ! use NumPY for everything! Performance!
# - TODO: Implement pays more when blackjack
# - TODO: Add SEVERAL small rules that can be found in https://en.wikipedia.org/wiki/Blackjack
#
# RULES and DETAILS:
# ==================
#
# - Dealer must hit if lower then 16. If ctHIT_ON_SOFT_HAND = True then see comment in the variable
# - Order of play: Dealer gives a card for each player, one for him face up. Then one again for each player and one for him again
# - If using more them one player, the results of them are combined averaged
# - If using more them one task, the results of them are combined averaged
# - The number of decks may be increased in order to accomodade the number of players
# - If the remaining cards in the deck are only 20%, then get new shuffled decks up tho the amount of decks defined in the param
# - If player blows, the dealer wins even before he plays (make a huge difference, giving more advantage to the dealer)
# - Can only split once, having 2 game at once
# - Can only split if the FIRST 1 cards are equal


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
ctSTRAT_ALGORITM = "BJ_BASIC_STRAT_FULL"

# Number of maches being simulated
ctNUM_MATCHES = 100000

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
ctNUM_PRECISION = 8

# Dealer must hit on soft 17 (when have an ACE and a 6) ? If not, will hit when sum of cards <= 16, else hit on <= 17 if have an ACE or hit when <= 16 when doesnt have an ACE
ctHIT_ON_SOFT_HAND = False

# Enable the player to split cards when he has a hand that are made of equal cards, on the first hand
ctUSE_SPLITTING = True


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

    def get_next_action(self, _force: str = None) -> str:

        ret = False

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
                ret = alg.blackjack_alg_BJ_BASIC_STRAT_FULL(self, ctHIT_ON_SOFT_HAND)

            elif self.algoritm == "BJ_BASIC_STRAT_NOSPLIT_NODOUBLE":
                ret = alg.blackjack_alg_BJ_BASIC_STRAT_NOSPLIT_NODOUBLE(self)

            elif self.algoritm == "MURCH":
                ret = alg.blackjack_alg_MURCH(self)

            elif self.algoritm == "SIMPLE":
                ret = alg.blackjack_alg_SIMPLE(self)

            # if has 21 or more, always say no to hit
            if self.get_card_sum() >= 21:
                ret = "STAND"

             # hard coded always and never, for tests. Last test so it prevales from any other test
            if self.algoritm == "NEVER":
                ret = "STAND"

            elif self.algoritm == "ALWAYS":
                ret = "HIT"

            return ret

        else:
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

        if len(self.cards) == 2:
            if self.cards[0][0] == self.cards[1][0]:
                return True

        return False

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def Main() -> None:

    print("Simulating", ctNUM_MATCHES, "match ..." if ctNUM_MATCHES == 1 else "matches ...")

    before_time = time()
    speed = 0

    run_simulation_project(ctNUM_MATCHES, ctPROCESSING_MODE, ctUSE_BETTING, ctNUM_PLAYERS)

    passed_time = time() - before_time

    if passed_time > 0:
        speed = ctNUM_MATCHES / passed_time

    print("Total time: ", round(passed_time, 2), "seconds -- " + str(round(speed, 2)) + " matches/s")


def run_simulation_project(num_matches: int = 1, processing_mode: str = "NORMAL", use_betting: bool = False, num_players: int = 1) -> None:
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

        win_ratio_simu = [simulate_matches([num_matches, processing_mode, use_betting, num_players])]

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
            p = multiprocessing.Process(target=simulate_matches, args=([num_matches_task, processing_mode, use_betting, num_players], i, return_dict))
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
        win_ratio_simu = pool.map(simulate_matches, [[num_matches_task, processing_mode, use_betting, num_players] for _ in range(0, ctNUM_SIMULTANEOUS_TASKS)])

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
            t = threading.Thread(target=simulate_matches, args=([num_matches_task, processing_mode, use_betting, num_players], i, return_dict))
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

    formated_result = mask.format(win_ratio_final[0]), mask.format(win_ratio_final[1]), mask.format(win_ratio_final[2])

    # formated_result = []
    # print (mask.format(win_ratio_final[0]))

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
    use_betting = params[2]
    num_players = params[3]

    total_win_player = [0 for _ in range(0, num_players)]
    total_win_dealer = [0 for _ in range(0, num_players)]
    total_win_push = [0 for _ in range(0, num_players)]

    # if the number of players (plus dealer) times 6 cards each is more then the avaliable cards, incrise deck number to support the game
    if (num_players + 1) * 6 >= ctNUM_OF_DECKS * 54:
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

    params_used = str(num_players) + " player(s), 1 Dealer, " + str(ctNUM_OF_DECKS) + " decks, Use betting: " + str(use_betting) + ", Betting Alg: " + ctBET_ALGORITM + ", Strategy Alg: " + ctSTRAT_ALGORITM + ", Processing mode: " + processing_mode

    if processing_mode != "NORMAL":
        params_used = params_used + " (Tasks: " + str(ctNUM_SIMULTANEOUS_TASKS) + ")"

    print(params_used)

    for x in range(0, num_matches):

        # if there are less then 20 cards in deck, get new decks
        if len(current_deck) <= int(ctNUM_OF_DECKS * 52 * 0.2):
            current_deck = new_deck(number_of_decks_used=ctNUM_OF_DECKS)

        # print(current_deck)

        winner = run_match(current_deck, aGamePlayers, use_betting)

        for conta_player in range(0, len(winner)):

            if winner[conta_player] == "PLAYER":
                total_win_player[conta_player] = total_win_player[conta_player] + 1

            elif winner[conta_player] == "DEALER":
                total_win_dealer[conta_player] = total_win_dealer[conta_player] + 1

            elif winner[conta_player] == "PUSH":
                total_win_push[conta_player] = total_win_push[conta_player] + 1

        if x > 9:
            win_ratio_player = (total_win_player[0] * 100) / x
            win_ratio_dealer = (total_win_dealer[0] * 100) / x
            win_ratio_push = (total_win_push[0] * 100) / x

            passed_time = time() - before_time

            if passed_time > 0:
                speed = x / (passed_time)
            # check_sum = win_ratio_player + win_ratio_dealer + win_ratio_push

            line = "RealTime: Player 1:  Win Ratio in " + "{:06d}".format(x + 1) + " games (player x dealer x push): " \
                + "{:.8f}".format(win_ratio_player) + ", " \
                + "{:.8f}".format(win_ratio_dealer) + ", " \
                + "{:.8f}".format(win_ratio_push)

            if use_betting:
                line += " -- Balance: P1$: {:.2f}".format(aGamePlayers[1].final_money) + " x {:.2f}".format(aGamePlayers[0].final_money) + " :D$"

            line += " -- Speed: {:.2f}".format(speed) + " matches/s"

            # if processing_mode in ["NORMAL"]:
            print_inline(line)

    if num_matches > 10:
        if processing_mode in ["NORMAL"]:
            print("")

    final_result = []

    for conta_player in range(0, num_players):

        win_ratio_player = (total_win_player[conta_player] * 100) / num_matches
        win_ratio_dealer = (total_win_dealer[conta_player] * 100) / num_matches
        win_ratio_push = (total_win_push[conta_player] * 100) / num_matches

        final_result.append((round(win_ratio_player, ctNUM_PRECISION), round(win_ratio_dealer, ctNUM_PRECISION), round(win_ratio_push, ctNUM_PRECISION)))

    if return_dict is not None:
        return_dict[index_proc] = final_result

    if use_betting:
        print("")
        print("BALANCE:")

        for conta_player in range(0, num_players + 1):
            print("Start: " + str("{:.2f}".format(round(aGamePlayers[conta_player].start_money, 2))) + " | End: " + str("{:.2f}".format(round(aGamePlayers[conta_player].final_money, 2))) + "   -- " + aGamePlayers[conta_player].name)
        print("")

    return final_result


def run_match(deck: list, arrGamePlayers: object, use_betting: bool = False) -> list:
    """
    runs one match between a dealer and players, using the deck in place at the moment
    returns a list with the result in N positions, 1 for each player, in order (player1, player2, etc)
    Ex.: 3 players. REsult: ["PLAYER", "PLAYER", "DEALER"] . In this result the player 1 and 2 won.. while the 
    player 3 lost.
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

        if use_betting is True:
            player.actual_bet = 0
            player.actual_bet_splitted = 0

    # if we are using bets, then, place bet
    if use_betting is True:

        for player in arrGamePlayers:
            if player.type != "DEALER":
                player.actual_bet = player.define_bet_value()

    # Players get 1 card
    # player.hit(deck)
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.hit(deck)

    # Dealer get 1 card face up
    # dealer.hit(deck)
    for dealer in arrGamePlayers:
        if dealer.type == "DEALER":
            dealer.hit(deck)

    # dealer reveals their first card to players
    # player.known_dealer_cards = dealer.cards[0]
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.known_dealer_cards = arrGamePlayers[0].cards[0]

    # Players get 1 more card
    # player.hit(deck)
    for player in arrGamePlayers:
        if player.type != "DEALER":
            player.hit(deck)

    # Dealer get 1 more card face down
    # dealer.hit(deck)
    for dealer in arrGamePlayers:
        if dealer.type == "DEALER":
            dealer.hit(deck)

    # player = GamePlayer(_name="Murch", _algoritm = "MURCH", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name="Murch", _algoritm = "SIMPLE", _cards=[get_card_from_deck(deck), get_card_from_deck(deck)])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck), get_card_from_deck(deck) ])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck, "K"), get_card_from_deck(deck, "8") ])

    # arrGamePlayers[0].cards = [['8', '♣'], ['10', '♦']]
    # arrGamePlayers[1].cards = [['K', '♣'], ['3', '♠'], ['6', '♣']]

    # arrGamePlayers[0].cards = [['6', '♥'], ['Q', '♦'], ['9', '♥']]
    # arrGamePlayers[1].cards = [['8', '♦'], ['6', '♣']]

    # arrGamePlayers[0].cards = [['8', '♥'], ['5', '♥'], ['7', '♠']]
    # arrGamePlayers[1].cards = [['3', '♦'], ['2', '♣'], ['4', '♥'], ['3', '♥'], ['K', '♣']]

    # arrGamePlayers[1].cards = [['A', '♣'], ['A', '♦'], ['K', '♦']]
    # arrGamePlayers[1].cards = [['A', '♥'], ['3', '♦'], ['4', '♠']]


    turn = "PLAYERS"

    while turn == "PLAYERS":

        for player in list(arrGamePlayers):
            if player.type != "DEALER":

                player_done = False

                while player_done is False:

                    check_hit = player.get_next_action()

                    if check_hit == "HIT":

                        player.hit(deck)

                    elif check_hit == "SPLIT":

                        player.hit(deck)

                    elif check_hit == "DOUBLE":

                        player.hit(deck)

                    elif check_hit == "SURRENDER":

                        player.hit(deck)

                    elif check_hit == "STAND":

                        player_done = True

                    if player.get_card_sum() > 21:

                        winner.append("DEALER")

                        player_done = True

                    else:
                        if player_done == True:
                            winner.append("STAND")

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

                        dealer_done = True

                        ls(dealer.name, "exploded!")

                    else:
                        if dealer_done == True:
                            # insert the result of the dealer in the 1st position of the result list
                            winner.insert(0, "STAND")

                    ls(dealer.name, ": check_hit =", check_hit, "| Cartas: ", dealer.print_hand(), dealer.get_card_sum())

        turn = "END"

    dealer_sum = 0
    player_sum = 0

    # check if dealer exploded. All players that are not exploded wins
    if winner[0] == "BLOW":

        for x in range(0, len(winner)):
            if x > 0:
                if winner[x] == "STAND":

                    winner[x] = "PLAYER"

                    if use_betting is True:
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet

                elif winner[x] == "DEALER":

                    if use_betting is True:
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

    else:

        for x in range(0, len(winner)):

            if x == 0:

                dealer_sum = arrGamePlayers[x].get_card_sum()

            else:

                player_sum = arrGamePlayers[x].get_card_sum()

            if x > 0:

                if winner[x] == "STAND":

                    if dealer_sum == player_sum:
                        winner[x] = "PUSH"

                    elif dealer_sum > player_sum:
                        winner[x] = "DEALER"

                        if use_betting is True:
                            arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                            arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

                    elif dealer_sum < player_sum:
                        winner[x] = "PLAYER"

                        if use_betting is True:
                            arrGamePlayers[0].final_money = arrGamePlayers[0].final_money - arrGamePlayers[x].actual_bet
                            arrGamePlayers[x].final_money = arrGamePlayers[x].final_money + arrGamePlayers[x].actual_bet

                elif winner[x] == "DEALER":

                    if use_betting is True:
                        arrGamePlayers[0].final_money = arrGamePlayers[0].final_money + arrGamePlayers[x].actual_bet
                        arrGamePlayers[x].final_money = arrGamePlayers[x].final_money - arrGamePlayers[x].actual_bet

    ls("Player FINAL hand:", player.print_hand(), player.get_card_sum())
    ls("dealer  FINAL hand:", dealer.print_hand(), dealer.get_card_sum())
    ls("WINNER:", winner)

    ls("=== FINAL ===========================================")

    ls("\n\n")

    # print(winner)
    # print(arrGamePlayers[0].cards)
    # print(arrGamePlayers[1].cards)

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

    if forceValue is None:
        return deck.pop()
    else:
        return [forceValue, "♥"]


if __name__ == "__main__":

    Main()

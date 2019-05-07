
import random as rnd

from bib_support import get_card_val

AVALIABLE_ALGS = ["NEVER", "ALWAYS", "50X50", "BJ_BASIC_STRAT_FULL", "BJ_BASIC_STRAT_NOSPLIT_NODOUBLE", "MURCH", "DEALER"]

# Default algoritm for the dealer. Follows the rules of the game for the dealer


def blackjack_alg_DEALER(caller: object, hit_on_soft_hand: bool = False) -> str:

    ret = None

    # num_of_aces = len([x[0] for x in caller.cards if x[0] == "A"])

    card_sum = caller.get_card_sum()

    if card_sum <= 16:

        ret = "HIT"

    elif card_sum == 17:

        if hit_on_soft_hand is False:
            ret = "STAND"
        else:
            ret = "HIT"

    else:

        ret = "STAND"

    return ret


def blackjack_alg_50X50() -> str:

    ret = None

    if rnd.randint(0, 1) == 0:
        ret = "STAND"
    else:
        ret = "HIT"

    return ret


def blackjack_alg_BJ_BASIC_STRAT_FULL(caller: object,
                                      hand_number: int,
                                      hit_on_soft: bool = False,
                                      allow_split: bool = True,
                                      allow_double: bool = False,
                                      allow_surrender: bool = False) -> str:

    # https://en.wikipedia.org/wiki/Blackjack#Basic_strategy

    if allow_split:
        if hand_number == 0:
            cards = caller.cards
        else:
            cards = caller.cards_splitted
    else:
        cards = caller.cards

    num_of_aces = len([x[0] for x in cards if x[0] == "A"])

    card_sum = caller.get_card_sum(_hand_number=hand_number)

    # we should never use this alg for the dealer beause the alg
    # depends on the dealer first card.. witch doesnt exists when
    # the dealer is being created. But, for testing, I will hard code
    # some random card for is this alg is being used by the dealer.
    # this random card probably fucks all the reality im trying to achieve
    # not random. fixed some card
    # The dealer has it own algoritm.
    if caller.type == "DEALER":
        known_dealer_card_value = get_card_val("7")
    else:
        known_dealer_card_value = get_card_val(caller.known_dealer_cards[0])

    ret = None

    # if has 21, its obvious: return stand
    if card_sum == 21:

        ret = "STAND"
        return ret

    found_pair_match = False
    found_total_match = False

    # check if we have a pair in the first hand, in the begining of the game
    if len(cards) == 2:

        pairs = []
        pairs.append(["A", len([x[0] for x in cards if x[0] == "A"])])
        pairs.append(["J", len([x[0] for x in cards if x[0] == "J"])])
        pairs.append(["Q", len([x[0] for x in cards if x[0] == "Q"])])
        pairs.append(["K", len([x[0] for x in cards if x[0] == "K"])])

        for k in range(2, 11):
            pairs.append([str(k), len([x[0] for x in cards if x[0] == str(k)])])

        for pair in pairs:

            #  PAIRS - BASIC STRATEGY:
            #  =======================
            #
            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> A,A         SP  SP  SP  SP  SP  SP  SP  SP  SP  SP
            # Player -> 10,10       S   S   S   S   S   S   S   S   S   S
            # Player -> 9,9         SP  SP  SP  SP  SP  S   SP  SP  S   S
            # Player -> 8,8         SP  SP  SP  SP  SP  SP  SP  SP  SP  SP
            # Player -> 7,7         SP  SP  SP  SP  SP  SP  H   H   H   H
            # Player -> 6,6         SP  SP  SP  SP  SP  H   H   H   H   H
            # Player -> 5,5         Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  H   H
            # Player -> 4,4         H   H   H   SP  SP  H   H   H   H   H
            # Player -> 2,2–3,3     SP  SP  SP  SP  SP  SP  H   H   H   H

                        # S = Stand
                        # H = Hit
                        # Dh = Double (if not allowed, then hit)
                        # Ds = Double (if not allowed, then stand)
                        # SP = Split
                        # SU = Surrender (if not allowed, then hit)

            if pair[1] >= 2:
                #           2   3   4   5   6   7   8   9   10  A
                # 2,2–3,3   SP  SP  SP  SP  SP  SP  H   H   H   H
                if pair[0] == "2" or pair[0] == "3":

                    if known_dealer_card_value in {2, 3, 4, 5, 6, 7}:
                        if allow_split:
                            ret = "SPLIT"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                    if known_dealer_card_value in {1, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 4,4       H   H   H   SP  SP  H   H   H   H   H
                if pair[0] == "4":

                    if known_dealer_card_value in {1, 2, 3, 4, 7, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                    if known_dealer_card_value in {5, 6}:
                        if allow_split:
                            ret = "SPLIT"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 5,5       Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  H   H
                if pair[0] == "5":

                    if known_dealer_card_value in {2, 3, 4, 5, 6, 7, 8, 9}:
                        if allow_double:
                            ret = "DOUBLE"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                    if known_dealer_card_value in {1, 10}:
                        ret = "HIT"
                        found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 6,6       SP  SP  SP  SP  SP  H   H   H   H   H
                if pair[0] == "6":

                    if known_dealer_card_value in {1, 7, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                    if known_dealer_card_value in {2, 3, 4, 5, 6}:
                        if allow_split:
                            ret = "SPLIT"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 7,7       SP  SP  SP  SP  SP  SP  H   H   H   H
                if pair[0] == "7":

                    if known_dealer_card_value in {1, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                    if known_dealer_card_value in {2, 3, 4, 5, 6, 7}:
                        if allow_split:
                            ret = "SPLIT"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 8,8       SP  SP  SP  SP  SP  SP  SP  SP  SP  SP
                if pair[0] == "8":
                    if allow_split:
                        ret = "SPLIT"
                        found_pair_match = True
                    else:
                        ret = "HIT"
                        found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 9,9       SP  SP  SP  SP  SP  S   SP  SP  S   S
                if pair[0] == "9":

                    if known_dealer_card_value in {1, 7, 10}:
                        ret = "STAND"
                        found_pair_match = True

                    if known_dealer_card_value in {2, 3, 4, 5, 6, 8, 9}:
                        if allow_split:
                            ret = "SPLIT"
                            found_pair_match = True
                        else:
                            ret = "HIT"
                            found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # 10,10     S   S   S   S   S   S   S   S   S   S
                if pair[0] == "10" or pair[0] == "J" or pair[0] == "Q" or pair[0] == "K":
                    ret = "STAND"
                    found_pair_match = True

                #           2   3   4   5   6   7   8   9   10  A
                # A,A       SP  SP  SP  SP  SP  SP  SP  SP  SP  SP
                if pair[0] == "A":
                    if allow_split:
                        ret = "SPLIT"
                        found_pair_match = True
                    else:
                        ret = "HIT"
                        found_pair_match = True

    # didnt find pairs. So try for a hard or soft hand
    if found_pair_match == False:

        if num_of_aces == 0:

            #  HARD HAND (excuding pairs) - BASIC STRATEGY:
            #  ============================================
            #
            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 17–20       S   S   S   S   S   S   S   S   S   S
            # Player -> 16          S   S   S   S   S   H   H   SU  SU  SU
            # Player -> 15          S   S   S   S   S   H   H   H   SU  H
            # Player -> 13–14       S   S   S   S   S   H   H   H   H   H
            # Player -> 12          H   H   S   S   S   H   H   H   H   H
            # Player -> 11          Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh
            # Player -> 10          Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  H   H
            # Player -> 9           H   Dh  Dh  Dh  Dh  H   H   H   H   H
            # Player -> 5–8         H   H   H   H   H   H   H   H   H   H

            # S = Stand
            # H = Hit
            # Dh = Double (if not allowed, then hit)
            # Ds = Double (if not allowed, then stand)
            # SP = Split
            # SU = Surrender (if not allowed, then hit)

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 5–8         H   H   H   H   H   H   H   H   H   H
            if card_sum <= 8:

                ret = "HIT"
                found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 9           H   Dh  Dh  Dh  Dh  H   H   H   H   H
            elif card_sum == 9:

                if known_dealer_card_value in {1, 2, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {3, 4, 5, 6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "HIT"
                    found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 10          Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  H   H
            elif card_sum == 10:

                if known_dealer_card_value in {1, 10}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {2, 3, 4, 5, 6, 7, 8, 9}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 11          Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh
            elif card_sum == 11:

                if allow_double:
                    ret = "DOUBLE"
                    found_total_match = True
                else:
                    ret = "HIT"
                    found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 12          H   H   S   S   S   H   H   H   H   H
            elif card_sum == 12:

                if known_dealer_card_value in {4, 5, 6}:

                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {1, 2, 3, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 13–14       S   S   S   S   S   H   H   H   H   H
            elif card_sum >= 13 and card_sum <= 14:

                if known_dealer_card_value in {2, 3, 4, 5, 6}:

                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {1, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 15          S   S   S   S   S   H   H   H   SU  H
            elif card_sum == 15:

                if known_dealer_card_value in {2, 3, 4, 5, 6}:

                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {1, 7, 8, 9}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {10}:

                    if allow_surrender:
                        ret = "SURRENDER"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 16          S   S   S   S   S   H   H   SU  SU  SU
            elif card_sum == 16:

                if known_dealer_card_value in {2, 3, 4, 5, 6}:

                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {7, 8}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {1, 9, 10}:

                    if allow_surrender:
                        ret = "SURRENDER"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 17–20       S   S   S   S   S   S   S   S   S   S
            elif card_sum >= 17 and card_sum <= 20:

                ret = "STAND"
                found_total_match = True

        else:

            #  SOFT HAND (excuding pairs) - BASIC STRATEGY:
            #  ============================================
            #
            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,9 (10 or 20)              S   S   S   S   S   S   S   S   S   S
            # Player -> A,8 (9 or 19)               S   S   S   S   Ds  S   S   S   S   S
            # Player -> A,7 (8 or 18)               Ds  Ds  Ds  Ds  Ds  S   S   H   H   H
            # Player -> A,6 (7 or 17)               H   Dh  Dh  Dh  Dh  H   H   H   H   H
            # Player -> A,4–A,5 (5-6 or 15-16)      H   H   Dh  Dh  Dh  H   H   H   H   H
            # Player -> A,2–A,3 (3-4 or 13-14)      H   H   H   Dh  Dh  H   H   H   H   H

            # if its an A and a 10 -> 21 and its covered in the begining

            # S = Stand
            # H = Hit
            # Dh = Double (if not allowed, then hit)
            # Ds = Double (if not allowed, then stand)
            # SP = Split
            # SU = Surrender (if not allowed, then hit)

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,2–A,3 (3-4 or 13-14)      H   H   H   Dh  Dh  H   H   H   H   H
            if (card_sum >= 3 and card_sum <= 4) or (card_sum >= 13 and card_sum <= 14):

                if known_dealer_card_value in {1, 2, 3, 4, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {5, 6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,4–A,5 (5-6 or 15-16)      H   H   Dh  Dh  Dh  H   H   H   H   H
            if (card_sum >= 5 and card_sum <= 6) or (card_sum >= 15 and card_sum <= 16):

                if known_dealer_card_value in {1, 2, 3, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {4, 5, 6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,6 (7 or 17)               H   Dh  Dh  Dh  Dh  H   H   H   H   H
            if card_sum == 7 or card_sum == 17:

                if known_dealer_card_value in {1, 2, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {3, 4, 5, 6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "HIT"
                        found_total_match = True

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,7 (8 or 18)               Ds  Ds  Ds  Ds  Ds  S   S   H   H   H
            if card_sum == 8 or card_sum == 18:

                if known_dealer_card_value in {1, 9, 19}:

                    ret = "HIT"
                    found_total_match = True

                if known_dealer_card_value in {2, 3, 4, 5, 6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "STAND"
                        found_total_match = True

                if known_dealer_card_value in {7, 8}:
                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {1, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,8 (9 or 19)               S   S   S   S   Ds  S   S   S   S   S
            if card_sum == 9 or card_sum == 19:

                if known_dealer_card_value in {6}:

                    if allow_double:
                        ret = "DOUBLE"
                        found_total_match = True
                    else:
                        ret = "STAND"
                        found_total_match = True

                if known_dealer_card_value in {1, 2, 3, 4, 5, 7, 8, 9, 10}:

                    ret = "STAND"
                    found_total_match = True

            # Dealer ->                             2   3   4   5   6   7   8   9   10  A
            # Player -> A,9 (10 or 20)              S   S   S   S   S   S   S   S   S   S
            if card_sum == 10 or card_sum == 20:

                ret = "STAND"
                found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 11          Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh  Dh
            if card_sum == 11:

                if allow_double:
                    ret = "DOUBLE"
                    found_total_match = True
                else:
                    ret = "HIT"
                    found_total_match = True

            # Dealer ->             2   3   4   5   6   7   8   9   10  A
            # Player -> 12          H   H   S   S   S   H   H   H   H   H
            if card_sum == 12:

                if known_dealer_card_value in {4, 5, 6}:

                    ret = "STAND"
                    found_total_match = True

                if known_dealer_card_value in {1, 2, 3, 7, 8, 9, 10}:

                    ret = "HIT"
                    found_total_match = True

    # # fall here only if didnt match any other rule above. CAN NOT get in ther.
    # # If it does, then i did something wrong with the algoritm because all
    # # possible cases are described above
    # if found_pair_match == False and found_total_match == False:
    #     if card_sum <= 15:
    #         ret = "HIT"
    #     else:
    #         ret = "STAND"

    # if ret == None:
    #     print(cards)

    return ret


def blackjack_alg_BJ_BASIC_STRAT_NOSPLIT_NODOUBLE(caller: object) -> str:

    # https://en.wikipedia.org/wiki/Blackjack#Basic_strategy

    num_of_aces = len([x[0] for x in caller.cards if x[0] == "A"])

    card_sum = caller.get_card_sum()

    # we should never use this alg for the dealer beause the alg
    # depends on the dealer first card.. witch doesnt exists when
    # the dealer is being created. But, for testing, I will hard code
    # some random card for is this alg is being used by the dealer.
    # this random card probably fucks all the reality im trying to achieve
    # not random. fixed some card
    # The dealer has it own algoritm.
    if caller.type == "DEALER":
        known_dealer_card_value = get_card_val("7")
    else:
        known_dealer_card_value = get_card_val(caller.known_dealer_cards[0])

    ret = None

    found_pair_match = False
    found_total_match = False

    # check if we have a pair in the first hand, in the begining of the game
    if len(caller.cards) == 2:

        pairs = []
        pairs.append(["A", len([x[0] for x in caller.cards if x[0] == "A"])])
        pairs.append(["J", len([x[0] for x in caller.cards if x[0] == "J"])])
        pairs.append(["Q", len([x[0] for x in caller.cards if x[0] == "Q"])])
        pairs.append(["K", len([x[0] for x in caller.cards if x[0] == "K"])])

        for k in range(2, 11):
            pairs.append([str(k), len([x[0] for x in caller.cards if x[0] == str(k)])])

        for pair in pairs:

            if pair[1] >= 2:

                if pair[0] == "2" or pair[0] == "3":
                    if known_dealer_card_value in {1, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                if pair[0] == "4":
                    if known_dealer_card_value in {1, 2, 3, 4, 7, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                if pair[0] == "5":
                    ret = "HIT"
                    found_pair_match = True

                if pair[0] == "6":
                    if known_dealer_card_value in {1, 7, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                if pair[0] == "7":
                    if known_dealer_card_value in {1, 8, 9, 10}:
                        ret = "HIT"
                        found_pair_match = True

                if pair[0] == "9":
                    if known_dealer_card_value in {1, 7, 10}:
                        ret = "STAND"
                        found_pair_match = True

                if pair[0] == "10":
                    ret = "STAND"
                    found_pair_match = True

    # didnt find pairs. So try for a hard or soft hand
    if found_pair_match == False:

        if num_of_aces == 0:

            # HARD HAND (excluding pairs):
            if card_sum <= 11:
                ret = "HIT"
                found_total_match = True

            elif card_sum == 12:
                if known_dealer_card_value >= 4 and known_dealer_card_value <= 6:
                    ret = "STAND"
                else:
                    ret = "HIT"

                found_total_match = True

            elif card_sum >= 13 and card_sum <= 16:
                if known_dealer_card_value >= 2 and known_dealer_card_value <= 6:
                    ret = "STAND"
                else:
                    ret = "HIT"

                found_total_match = True

            elif card_sum >= 17 and card_sum <= 21:
                ret = "STAND"
                found_total_match = True

        else:
            # SOFT HAND (excluding pairs):

            if card_sum >= 13 and card_sum <= 17:
                ret = "HIT"
                found_total_match = True

            elif card_sum == 18:
                if known_dealer_card_value in {1, 9, 10}:
                    ret = "HIT"
                else:
                    ret = "STAND"

                found_total_match = True

            elif card_sum >= 19:
                ret = "STAND"
                found_total_match = True

            #  bellow seams to improve player win i dont know why
            # ret = "STAND"
            # found_total_match = True

    # fall here only if didnt match any other rule above
    if found_pair_match == False and found_total_match == False:
        if card_sum <= 15:
            ret = "HIT"
        else:
            ret = "STAND"

    return ret


def blackjack_alg_MURCH(caller: object) -> str:

    # from my guts

    card_sum = caller.get_card_sum()

    # we should never use this alg for the dealer beause the alg
    # depends on the dealer first card.. witch doesnt exists when
    # the dealer is being created. But, for testing, I will hard code
    # some random card for is this alg is being used by the dealer.
    # this random card probably fucks all the reality im trying to achieve
    # not random. fixed some card
    # The dealer has it own algoritm.
    if caller.type == "DEALER":
        known_dealer_card_value = get_card_val("7")
    else:
        known_dealer_card_value = get_card_val(caller.known_dealer_cards[0])

    ret = None

    if card_sum <= 13:
        ret = "HIT"
    elif card_sum > 13 and card_sum <= 17:
        if known_dealer_card_value == 1:
            ret = "HIT"
        else:
            if card_sum <= 16:
                ret = "HIT"
            else:
                ret = "STAND"
    else:

        ret = "STAND"

    return ret


def blackjack_alg_SIMPLE(caller: object) -> str:

    # from my guts2

    card_sum = caller.get_card_sum()

    ret = None

    if card_sum <= 17:
        ret = "HIT"

    else:

        ret = "STAND"

    return ret



# Default algoritm for betting
def blackjack_alg_BET_DEFAUT(caller: object, hit_on_soft_hand: bool = False) -> float:

    ret = None

    num_of_aces = len([x[0] for x in caller.cards if x[0] == "A"])

    card_sum = caller.get_card_sum()

    ret = 10.0

    return ret

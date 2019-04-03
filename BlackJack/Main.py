
import random as rnd



def shoud_hit(actual_cards: tuple, player_total: int, caller: str = "PLAYER") -> bool:

    """
    Function that returns if the player or table should ask for another card or not
    """



    if caller == "PLAYER":
        retFunc = False
    else:
        retFunc = False


    return retFunc


def simulate_game(num_games: int = 1) -> tuple:

    """
    Simulate N games and return the win rate for player and table
    Returns a tuple with player, table win rate
    """

    for x in range(1, num_games):

        player_card1 = rnd.randint(1, 13)
        player_card2 = rnd.randint(1, 13)

        table_card1 = rnd.randint(1, 13)
        table_card2 = rnd.randint(1, 13)

        player_doHit = shoud_hit([player_card1, player_card2], "PLAYER")

        while player_doHit == True:

            hit_card = rnd.randint(1, 13)





import random as rnd


class GamePlayer:

    def __init__(self, _name: str, _type: str = "PLAYER", _algoritm: str = "LUCKY", _cards: list = []):
        self.name = _name
        self.type = _type
        self.cards = _cards
        self.algoritm = _algoritm


    def hit(self, _card: int = rnd.randint(1, 13)) -> None:
        self.cards.append(_card)


    def should_hit(self, _force: bool = None) -> bool:

        if _force is None:

            if self.algoritm not in ["LUCKY", "AVG", "NEVER", "ALWAYS"]:
                self.algoritm = "LUCKY"


            if self.algoritm == "LUCKY":

                if rnd.randint(0, 1) == 0:
                    return False
                else:
                    return True


            elif self.algoritm == "NEVER":
                return False

            elif self.algoritm == "ALWAYS":
                return True

            elif self.algoritm == "AVG":
                pass


        else:
            return _force




def run_match() -> str:

    winner = "PLAYER"


    player = GamePlayer(_name = "Murch", _cards = [rnd.randint(1, 13), rnd.randint(1, 13)])
    table = GamePlayer(_name="Blacu Jacku", _cards=[rnd.randint(1, 13), rnd.randint(1, 13)], _type = "TABLE")



    print("=== MATCH ===========================================")
    print("Player INIT hand:", player.cards)
    print("Table  INIT hand:", table.cards)

    print("-----------------------------------------------------")

    check_hit = player.should_hit()
    print("PLAYER: check_hit =", check_hit, "| Cartas: ", player.cards)



    while check_hit == True:
        player.hit()

        check_hit = player.should_hit()
        print("PLAYER: check_hit =", check_hit, "| Cartas: ", player.cards)

    print("-----------------------------------------------------")


    check_hit = table.should_hit()
    print("TABLE: check_hit =", check_hit, "| Cartas: ", table.cards)

    while check_hit == True:
        table.hit()

        check_hit = table.should_hit()
        print("TABLE: check_hit =", check_hit, "| Cartas: ", table.cards)

    print("-----------------------------------------------------")


    print("Player FINAL hand:", player.cards)
    print("Table  FINAL hand:", table.cards)

    print("=== FINAL ===========================================")

    print("\n\n")
    # print(player.should_hit())

    # print(gPlayer1.cards)
    #
    # gPlayer1.add_card()
    #
    # print(gPlayer1.cards)



    return winner

def simulate_matches(num_matches = 1) -> tuple:

    total_win_player = 0
    total_win_table = 0


    for x in range(0, num_matches):

        winner = run_match()

        if winner == "PLAYER":
            total_win_player = total_win_player + 1
        else:
            total_win_table = total_win_table + 1


    win_ratio_player = (total_win_player * 100) / num_matches
    win_ratio_table = 100 - win_ratio_player

    return win_ratio_player, win_ratio_table

def Main() -> None:
    """
    Main function
    """

    num_matches = 10

    win_ratio = simulate_matches(num_matches)

    print("Win Ratio in", num_matches, "games (player x table): ", win_ratio)



    pass



if __name__ == "__main__":
    Main()
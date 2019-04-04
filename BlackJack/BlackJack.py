import random as rnd


gDebugMode = True



class GamePlayer:

    def __init__(self, _name: str, _type: str = "PLAYER", _algoritm: str = "LUCKY", _cards: list = []):
        self.name = _name
        self.type = _type
        self.cards = _cards
        self.algoritm = _algoritm


    def hit(self, _card: list) -> None:
        self.cards.append(_card)

    def print_hand(self) -> list:

        # return [ x[0] + "|" + x[1] + "|" + str(get_card_val(x[0])) for x in self.cards ]
        # return [ x[0] + "|" + x[1] for x in self.cards ]
        # return [ x[0] + " " + str(get_card_val(x[0])) +  x[1] for x in self.cards ]


        return [ x[0] + x[1] for x in self.cards ]


    def get_card_sum(self) -> int:

        num_of_aces = len( [ x[0] for x in self.cards if x[0] == "A" ] )

        if num_of_aces <= 1:
            value_for_ace = 11
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

        if _force is None:

            if self.algoritm not in ["LUCKY", "MAGIC", "NEVER", "ALWAYS"]:
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

            elif self.algoritm == "MAGIC":
                pass

        else:
            return _force

def get_card_from_deck(deck: list, forceValue: str = None) -> list:
    if forceValue is None:
        return deck.pop()
    else:
        return [forceValue, "♥"]


def get_card_val(card: str) -> int:
    """
    gets the value from a card. A = 1, figures = 10 and other are their numbers

    :param card:
    :return: int
    """


    if card[0] == "A":
        return 1

    elif card[0] == "J":
        return 11

    elif card[0] == "Q":
        return 12

    elif card[0] == "K":
        return 13

    else:
        return int(card)


def ls(val_to_print, *args) -> None:
    """
    helper function to print log mesagens on the terminal only if log mode is on
    :param val_to_print:
    :param args:
    :return:
    """
    if gDebugMode == True: print(val_to_print, *args)



def new_deck(shuffled: bool = True) -> list:

    # _deck = [ ["A", "OUROS"], ["7", "ESPADAS"] ]

    values = [ str(x) for x in range(2, 11) ] + ["J", "Q", "K", "A"]

    # suits = ["OUROS", "ESPADAS", "COPAS", "PAUS"] # ♥♦♣♠
    suits = ["♦", "♠", "♥", "♣"] # ♥♦♣♠

    deck = [[value, suit] for value in values for suit in suits]

    if shuffled == True:
        rnd.shuffle(deck)

    return deck




def run_match(deck: list) -> str:

    if rnd.randint(0, 1) == 0:
        winner = "PLAYER"
    else:
        winner = "TABLE"



    # Define player and table
    player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck), get_card_from_deck(deck) ])
    # player = GamePlayer(_name = "Murch", _cards = [ get_card_from_deck(deck, "A"), get_card_from_deck(deck, "A") ])
    table = GamePlayer(_name = "Blacu Jacku", _cards = [ get_card_from_deck(deck) ], _type = "TABLE")



    ls("=== MATCH ===========================================")
    ls("Player INIT hand:", player.print_hand(), player.get_card_sum())
    ls("Table  INIT hand:", table.print_hand(), table.get_card_sum())

    ls("-----------------------------------------------------")


    




    check_hit = player.should_hit()

    ls("PLAYER: check_hit =", check_hit, "| Cartas: ", player.print_hand(), player.get_card_sum())



    while check_hit == True:

        player.hit(get_card_from_deck(deck))

        check_hit = player.should_hit()

        ls("PLAYER: check_hit =", check_hit, "| Cartas: ", player.print_hand(), player.get_card_sum())




    ls("-----------------------------------------------------")


    check_hit = table.should_hit()

    ls("TABLE: check_hit =", check_hit, "| Cartas: ", table.print_hand(), table.get_card_sum())

    while check_hit == True:
        table.hit(get_card_from_deck(deck))

        check_hit = table.should_hit()
        ls("TABLE: check_hit =", check_hit, "| Cartas: ", table.print_hand(), table.get_card_sum())

    ls("-----------------------------------------------------")




    ls("Player FINAL hand:", player.print_hand(), player.get_card_sum())
    ls("Table  FINAL hand:", table.print_hand(), table.get_card_sum())

    ls("=== FINAL ===========================================")

    ls("\n\n")
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

        current_deck = new_deck()

        # print(current_deck)


        winner = run_match(current_deck)

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
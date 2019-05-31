
from sys import stdout


gDebugMode = False


def get_card_val(card: str) -> int:
    """
    gets the value from a card. A = 1, figures = 10 and other are their numbers

    :param card:
    :return: int
    """

    if card[0] == "A":
        return 1

    elif card[0] == "J":
        return 10

    elif card[0] == "Q":
        return 10

    elif card[0] == "K":
        return 10

    else:
        return int(card)


def ls(val_to_print, *args) -> None:
    """
    helper function to print log mesagens on the terminal only if log mode is on
    :param val_to_print:
    :param args:
    :return:
    """



    if gDebugMode == True:
        print(val_to_print, *args)


def print_inline(data: str, newline: bool = False) -> None:

    # pass

    stdout.write("\r%s" % data)
    stdout.flush()

    if newline:
        pass
        # stdout.write("\n")


import random


class Dice:
    def roll(self):
        valor1 = random.randint(1, 6)
        valor2 = random.randint(1, 6)

        return valor1, valor2


dado1 = Dice()
dado2 = Dice()
print(dado1.roll())
print(dado2.roll())







import random as rnd
import datetime as dt

import time


def gera_cpf(**params):


    if "cpf" in params:

        Algs = params["cpf"]

    else:

        Algs = [
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9),
            rnd.randint(0, 9)


        ]




    # Algs = [2,5,6,3,2,0,7,1,8]

    dig1 = Algs[0] * 10 + Algs[1] * 9 + Algs[2] * 8 + Algs[3] * 7 + Algs[4] * 6 + Algs[5] * 5 + Algs[6] * 4 + Algs[7] * 3 + Algs[8] * 2

    dig1 = 11 - dig1 % 11

    if dig1 >= 10: dig1 = 0

    dig2 = Algs[0] * 11 + Algs[1] * 10 + Algs[2] * 9 + Algs[3] * 8 + Algs[4] * 7 + Algs[5] * 6 + Algs[6] * 5 + Algs[7] * 4 + Algs[8] * 3 + dig1 * 2

    dig2 = 11 - dig2 % 11

    if dig2 >= 10: dig2 = 0

    ret = str(Algs[0]) + str(Algs[1]) + str(Algs[2]) + str(Algs[3]) + str(Algs[4]) + str(Algs[5]) + str(Algs[6]) + str(Algs[7]) + str(Algs[8]) + str(dig1) + str(dig2)


    return ret

i = 1

time_inicio = dt.datetime.now()


oldtime = time.time()



pode_sair = False

digits = 9

while pode_sair == False:
# while gera_cpf() != "25632071855":


    # if time.time() - oldtime < 0:
    #     the_cpf = gera_cpf(cpf = [2,5,6,3,2,0,7,1,8])
    # else:
    #     the_cpf = gera_cpf()
    #
    # if the_cpf[0:digits] == "25632071855"[0:digits]:
    #
    #     pode_sair = True


    the_cpf = gera_cpf()

    if the_cpf[0:digits] == "25632071855"[0:digits]:

        pode_sair = True

    # print(i)


    i = i + 1

else:

    time_fim = dt.datetime.now()

    print("i = " + str(i))

    print("CPF: " + the_cpf)


print ("Localizado !")

print ("Tempo: " + str(time_fim - time_inicio))
# for x in range(0, 11):
#
#     print(gera_cpf())
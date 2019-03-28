import random as ran

continua_jogo = True

placar_user = 0
placar_comp = 0

print("")
print("Bem vindo ao Jokempo!")
print ("Placar atual: Computador " + str(placar_comp) + " x " + str(placar_user) + " Voce")
print("")


while continua_jogo:

    vencedor = ""

    opcao = input("Digite sua opcao (R = Pedra, P = Papel, T = Tesoura  --  S = Sair) : ")
    opcao = opcao.upper()


    if opcao == "S":
        continua_jogo = False
    else:
        int_opcao_comp = ran.randint(1, 3)  # 1 = R, 2 = P, 3 = T

        #TODO: teste de todo
        #FIXME: teste de fixme


        if int_opcao_comp == 1:

            if opcao == "R":
                print ("Computador: Pedra -- Voce: Pedra -- Resultado: EMPATE")

            elif opcao == "P":
                print ("Computador: Pedra -- Voce: Papel -- Resultado: VOCE GANHA")
                placar_user = placar_user + 1

            elif opcao == "T":
                print ("Computador: Pedra -- Voce: Tesoura -- Resultado: COMPUTADOR GANHA")
                placar_comp = placar_comp + 1
            else:
                print ("Opcao Invalida. Digite R, P ou T")

        elif int_opcao_comp == 2:

            if opcao == "R":
                print ("Computador: Papel -- Voce: Pedra -- Resultado: COMPUTADOR GANHA")
                placar_comp = placar_comp + 1

            elif opcao == "P":
                print ("Computador: Papel -- Voce: Papel -- Resultado: EMPATE")

            elif opcao == "T":
                print ("Computador: Papel -- Voce: Tesoura -- Resultado: VOCE GANHA")
                placar_user = placar_user + 1
            else:
                print ("Opcao Invalida. Digite R, P ou T")

        elif int_opcao_comp == 3:

            if opcao == "R":
                print ("Computador: Tesoura -- Voce: Pedra -- Resultado: VOCE GANHA")
                placar_user = placar_user + 1

            elif opcao == "P":
                print ("Computador: Tesoura -- Voce: Papel -- Resultado: COMPUTADOR GANHA")
                placar_comp = placar_comp + 1

            elif opcao == "T":
                print ("Computador: Tesoura -- Voce: Tesoura -- Resultado: EMPATE")

            else:
                print ("Opcao Invalida. Digite R, P ou T")

    print ("Placar atual: Computador " + str(placar_comp) + " x " + str(placar_user) + " Voce")
    print("")


print("")
print ("Jogo finalizado")




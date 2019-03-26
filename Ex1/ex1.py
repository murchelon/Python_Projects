
from datetime import datetime



name = input("Digite seu nome: ")
age = input("Digite sua idade: ")
times = int(input("Quantas vezes devo repetir ? "))

year = datetime.now().year

year100 = 100 - int(age) + year

for x in range(times):
    print(name + ", vce tera 100 em " + str(year100))
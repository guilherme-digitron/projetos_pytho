import random
import os

letrasmin = ["a","b", "c", "d", "e", "f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"] 
letrasmax = ["A","B", "C", "D", "E", "F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
simbolos = [".","@","#","$","!","&"]
numeros = [1,2,3,4,5,6,7,8,9,0]
senha = "" 
aprovado = True

while aprovado:
    print("quantos caracteres deseja na senha ? \n")
    char = int(input("digite aqui:"))
    if char < 8:
        print("sua senha e muito pequena \n")
    else:
        aprovado = False


for i in range(char - 4):
    type_char = random.randint(1,4)

    if type_char == 1:
        new_char = random.choice(letrasmin)
    elif type_char == 2:
        new_char = random.choice(letrasmax)
    elif type_char == 3:
        new_char = random.choice(simbolos)
    else:
        new_char = str(random.choice(numeros))
    
    senha += new_char
senha += random.choice(letrasmin) + random.choice(letrasmax) + random.choice(simbolos) + str(random.choice(numeros))
senha = list(senha)
random.shuffle(senha)
senha = "".join(senha)

print(f"Sua senha e: {senha} \n")

salvar = int(input("1 - Salvar senha \n2 - Descartar Senha\nResposta: "))

if salvar == 1:
    obs = input("Digite aqui sua observação: ")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    arquivo = os.path.join(desktop, "registros.txt")

    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(f"{obs} {senha} \n")
    print("Sua senha foi salva com sucesso")
else:
    print("Senha descartada com sucesso")

import random

p = random.randint(1, 26)
def cesar(texto, p):
    cifra = ''
    for i in range(len(texto)):
        char = texto[i]
        if(char.isupper()):
            cifra += chr((ord(char) + p - 65) % 26 + 65)
        else:
            cifra += chr((ord(char) + p - 97) % 26 + 97)
    return cifra
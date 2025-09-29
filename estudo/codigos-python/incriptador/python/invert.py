

def invert(texto):
    cifra = ""
    i = len(texto) - 1
    while i >= 0:
        cifra = cifra + texto[i]
        i = i - 1
    return cifra

#:D
import random
import cesar
import invert
import rsa
from rsa import criptografar
from rsa import gerar_chaves

print("Hello World")
metod = input("digite o metodo de criptorafia:")
mensage = "Hello World"   

if metod == "c":
    print(cesar.cesar(mensage, cesar.p))
if metod == "i":
    print(invert.invert(mensage))
if metod == "rsa":

    criptografar_menssage = criptografar.Criptografia()
    result = criptografar_menssage.encripta_mensagem(mensage)
    print("criptografia:" + result)
    pass
from gerador_primos import GeradorPrimos
from gerar_chaves import Chaves
from criptografar import Criptografia

p = GeradorPrimos()
numero_p = p.numero_primo
print("\n P: ", str(numero_p))

q = GeradorPrimos()
numero_q = q.numero_primo
print("\n Q: ", str(numero_q))

chaves = Chaves(numero_p, numero_q)
chaves.gerar_chaves()

encripta = chaves.encripta_mensagem()
chaves.decripta_mensagem(encripta)

import math
import random

print('Bem vindo a Alexandria')
print('qual tomo deseja acessar ?')
ex = int(input('digite o numero do exemplar: '))

def cd1():

    N= int(input('digite quantas notas quer inserir: '))
    loop = 0
    nota = 0
    vnota =0
    while N>loop:
    
        vnota = int(input('digite sua nota: '))
        nota = nota + vnota
        loop = loop + 1
    
    print(nota/N)
    print('essa e sua media')
    
    
def cd2():
    c1 = float(input ('qual o cateto 1: '))
    c2 = float(input ('qual o cateto 2: '))
    h = math.sqrt(c1**2+c2**2)
    print(f'sua hipotenusa e {h}')
    
    
def cd3():
    an = float(input('digite um angulo'))
    sen = math.sin(math.radians(an))
    print('o ângulo de {} tem o seno de {:.2f}'. format(an, sen))
    
    cos = math.cos(math.radians(an))
    print('o ângulo de {} tem o cosseno de {:.2f}'. format(an, cos))
    
    tan = math.tan(math.radians(an))
    print('o ângulo de {} tem a tangente de {:.2f}'. format(an, tan))
    
    
def cd4():
    
   escolha = input('cara ou coroa ? ca/co :')
   possibilidades = ['ca', 'co']
   resultado = random.choice(possibilidades)
   if resultado == escolha:
    print('acertou')
   else:
    t = input('errou, o certo era {}, quer tentar novamente ? y/n :'.format(resultado))
    if t == 'y':
        cd4()
    else: 
        print('fim de jogo')
    
    
def cd5():
    
    elementos = int(input('digite o numero de participantes do sorteio: '))
    lista = list(range(1, elementos +1))
    random.shuffle(lista)
    print('o sorteio ficou {}'.format(lista))
#execucao

while True:

    if ex == 1:
        cd1()
        ex = int(input('digite o numero do exemplar: '))
        
    if ex == 2:
        cd2()
        ex = int(input('digite o numero do exemplar: '))
        
    if ex == 3:
        cd3()
        ex = int(input('digite o numero do exemplar: '))
            
    if ex == 4:
        cd4()
        ex = int(input('digite o numero do exemplar: '))
        
    if ex == 5:
        cd5()
        ex = int(input('digite o numero do exemplar: '))
            
    if ex <= 0 or ex >5:
        print('invalido')
        ex = int(input('digite o numero do exemplar: '))
        
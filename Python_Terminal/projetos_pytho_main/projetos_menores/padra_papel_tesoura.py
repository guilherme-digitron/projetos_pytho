import random

execute = True
point = 0
pointM = 0
player_history = []

def maquina_esperta():
    if len(player_history) < 2:
        return random.randint(1, 3)
    
    pedra = player_history.count(1)
    papel = player_history.count(2)
    tesoura = player_history.count(3)

    # Prever a jogada mais comum do jogador
    if pedra >= papel and pedra >= tesoura:
        return 2  # papel vence pedra
    elif papel >= pedra and papel >= tesoura:
        return 3  # tesoura vence papel
    else:
        return 1  # pedra vence tesoura

while True:

    while not execute:
        print('    Reiniciando')
        point = 0
        pointM = 0
        player_history = []
        execute = True

    while execute:
        print('    Jogar pedra, papel ou tesoura ?')
        choice = input('    y/n\n')
        choiceM = 0

        if choice == 'y':
            print(f'    O placar está {point} para você e {pointM} para mim')
            print('    Faça sua escolha:')
            print('    1: PEDRA')
            print('    2: PAPEL')
            print('    3: TESOURA')
            choice = input()

        elif choice == 'n':
            print('OK')
            execute = False
            continue

        else:
            print('Erro')
            execute = False
            break

        if choice not in ['1', '2', '3']:
            print('Erro')
            execute = False
            break

        choice = int(choice)
        player_history.append(choice)

        # Sua escolha
        if choice == 1:
            print("""    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)""")

        elif choice == 2:
            print("""     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)""")

        elif choice == 3:
            print("""    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)""")

        # Escolha da máquina com IA
        print('    Eu escolhi:')
        choiceM = maquina_esperta()

        if choiceM == 1:
            print("""    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)""")

        elif choiceM == 2:
            print("""     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)""")

        elif choiceM == 3:
            print("""    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)""")

        # Resultado
        if choice == choiceM:
            print('    Empate')
        elif (choice == 1 and choiceM == 3) or \
             (choice == 2 and choiceM == 1) or \
             (choice == 3 and choiceM == 2):
            print('    Você ganhou')
            point += 1
        else:
            print('    Você perdeu')
            pointM += 1
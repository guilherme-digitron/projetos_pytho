#!/usr/bin/env python3
"""
Gerador de Senhas Seguro - Versão Refatorada
Gera senhas fortes com letras, números e símbolos
Salva opcionalmente em registros.txt na Área de Trabalho
"""

import random
import os
import argparse
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Cores (apenas na saída, nunca nos inputs)
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
W = Fore.WHITE
DIM = Style.DIM
RESET = Style.RESET_ALL

# Conjuntos de caracteres
LETRAS_MIN = list("abcdefghijklmnopqrstuvwxyz")
LETRAS_MAI = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
NUMEROS    = list("0123456789")
SIMBOLOS   = list("!@#$%^&*()-_=+[]{}|;:',.<>?/`~")

# Garantimos pelo menos um de cada tipo
TIPOS_OBRIGATORIOS = [
    random.choice(LETRAS_MIN),
    random.choice(LETRAS_MAI),
    random.choice(NUMEROS),
    random.choice(SIMBOLOS)
]


def gerar_senha(tamanho: int) -> str:
    """Gera uma senha forte com pelo menos 1 de cada tipo de caractere"""
    if tamanho < 8:
        raise ValueError("O tamanho mínimo recomendado é 8 caracteres")

    # Começa com os 4 caracteres obrigatórios
    senha_lista = TIPOS_OBRIGATORIOS.copy()

    # Preenche o restante
    todos_caracteres = LETRAS_MIN + LETRAS_MAI + NUMEROS + SIMBOLOS

    for _ in range(tamanho - 4):
        senha_lista.append(random.choice(todos_caracteres))

    # Embaralha tudo
    random.shuffle(senha_lista)

    return "".join(senha_lista)


def salvar_senha(senha: str, observacao: str):
    """Salva a senha + observação no arquivo registros.txt na Área de Trabalho"""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    caminho = os.path.join(desktop, "registros_senhas.txt")

    try:
        with open(caminho, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{observacao.strip()} | {senha}\n")
        print(f"{G}Senha salva com sucesso em:{RESET}")
        print(f"   {caminho}")
    except Exception as e:
        print(f"{R}Erro ao salvar senha: {e}{RESET}")


def show_menu():
    print(f"\n{C}Gerador de Senhas Seguras{RESET}")
    print("-" * 45)
    print(f" {G}1{Y}  Gerar nova senha")
    print(f" {G}2{Y}  Gerar várias senhas de uma vez")
    print(f" {R}0{Y}  Sair")
    print("-" * 45)


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de senhas fortes",
        epilog="""
Exemplos:
  python gerador_senhas.py --tamanho 16
  python gerador_senhas.py --tamanho 12 --quantidade 5
        """
    )
    parser.add_argument("--tamanho", type=int, default=0, help="Tamanho da senha")
    parser.add_argument("--quantidade", type=int, default=1, help="Quantas senhas gerar (modo batch)")

    args = parser.parse_args()

    # Modo CLI (argumentos passados)
    if args.tamanho > 0:
        try:
            for i in range(args.quantidade):
                senha = gerar_senha(args.tamanho)
                print(f"{Y}Senha {i+1:02d}:{RESET}  {senha}")
        except ValueError as e:
            print(f"{R}Erro: {e}{RESET}")
        return

    # Modo interativo
    while True:
        show_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print(f"{Y}Saindo...{RESET}")
            break

        elif opcao == "1":
            while True:
                try:
                    tamanho_str = input("Quantos caracteres deseja na senha? (mínimo 8): ").strip()
                    tamanho = int(tamanho_str)
                    if tamanho < 8:
                        print(f"{R}O tamanho mínimo recomendado é 8 caracteres.{RESET}")
                        continue
                    break
                except ValueError:
                    print(f"{R}Digite um número válido.{RESET}")

            try:
                senha = gerar_senha(tamanho)
                print(f"\n{G}Sua senha gerada:{RESET}")
                print(f"   {senha}\n")

                salvar = input("Deseja salvar esta senha? (s/n): ").strip().lower()
                if salvar in ("s", "sim", "y", "yes"):
                    obs = input("Digite uma observação (ex: Gmail 2025, Netflix, etc): ").strip()
                    if obs:
                        salvar_senha(senha, obs)
                    else:
                        print(f"{Y}Observação vazia → senha não foi salva.{RESET}")
                else:
                    print(f"{Y}Senha descartada.{RESET}")

            except ValueError as e:
                print(f"{R}Erro: {e}{RESET}")

        elif opcao == "2":
            try:
                qtd = int(input("Quantas senhas deseja gerar? (1–20): ").strip())
                if not 1 <= qtd <= 20:
                    print(f"{R}Digite um número entre 1 e 20.{RESET}")
                    continue

                tam = int(input("Tamanho de cada senha (mínimo 8): ").strip())
                if tam < 8:
                    print(f"{R}Tamanho mínimo é 8.{RESET}")
                    continue

                print(f"\n{G}Gerando {qtd} senhas de {tam} caracteres...{RESET}\n")
                for i in range(qtd):
                    senha = gerar_senha(tam)
                    print(f"  {i+1:02d} → {senha}")

            except ValueError:
                print(f"{R}Entrada inválida.{RESET}")

        else:
            print(f"{R}Opção inválida.{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Programa interrompido.{RESET}")
    except Exception as e:
        print(f"{R}Erro inesperado: {e}{RESET}")
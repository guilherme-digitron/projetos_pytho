import re
import math
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class BhaskaraCalculator:
    """Calculadora de equações do segundo grau usando a fórmula de Bhaskara"""
    
    def __init__(self):
        self.equacao_original = ""
        self.a = 0
        self.b = 0
        self.c = 0
        self.delta = 0
    
    def mostrar_banner(self):
        """Mostra o banner da calculadora"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}          CALCULADORA DE BHASKARA")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def mostrar_instrucoes(self):
        """Mostra as instruções de uso"""
        print(f"{Fore.GREEN}📋 INSTRUÇÕES:{Style.RESET_ALL}")
        print(f"   • Digite a equação no formato: {Fore.YELLOW}ax^2+bx+c=0{Style.RESET_ALL}")
        print(f"   • Exemplos válidos:")
        print(f"      {Fore.CYAN}2x^2-3x+1=0{Style.RESET_ALL}")
        print(f"      {Fore.CYAN}x^2+5x-6=0{Style.RESET_ALL}")
        print(f"      {Fore.CYAN}-3x^2+2x+8=0{Style.RESET_ALL}")
        print(f"   • Você pode usar espaços ou não")
        print(f"   • Use {Fore.RED}+ ou -{Style.RESET_ALL} entre os termos\n")
    
    def extrair_coeficientes(self, equacao):
        """
        Extrai os coeficientes a, b e c da equação
        Retorna (a, b, c) ou None se formato inválido
        """
        self.equacao_original = equacao
        equacao = equacao.replace(" ", "").lower()
        
        # Padrão para capturar ax^2 + bx + c = 0
        padrao = r"([-+]?\d*)x\^2([-+]?\d*)x?([-+]?\d*)=0"
        match = re.match(padrao, equacao)
        
        if not match:
            return None
        
        a, b, c = match.groups()
        
        # Trata coeficiente 'a'
        if a == "" or a == "+":
            a = 1
        elif a == "-":
            a = -1
        else:
            a = int(a)
        
        # Trata coeficiente 'b'
        if b == "" or b == "+":
            b = 1
        elif b == "-":
            b = -1
        elif b:
            b = int(b)
        else:
            b = 0
        
        # Trata coeficiente 'c'
        c = int(c) if c else 0
        
        self.a, self.b, self.c = a, b, c
        return a, b, c
    
    def calcular_delta(self):
        """Calcula o discriminante (delta)"""
        self.delta = self.b**2 - 4*self.a*self.c
        return self.delta
    
    def resolver(self):
        """
        Resolve a equação e retorna o resultado formatado
        """
        # Mostra a equação interpretada
        print(f"\n{Fore.MAGENTA}📐 Equação interpretada:{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}{self.formatar_equacao()}{Style.RESET_ALL}")
        
        # Mostra os coeficientes
        print(f"\n{Fore.MAGENTA}📊 Coeficientes:{Style.RESET_ALL}")
        print(f"   a = {Fore.YELLOW}{self.a}{Style.RESET_ALL}")
        print(f"   b = {Fore.YELLOW}{self.b}{Style.RESET_ALL}")
        print(f"   c = {Fore.YELLOW}{self.c}{Style.RESET_ALL}")
        
        # Calcula delta
        self.calcular_delta()
        print(f"\n{Fore.MAGENTA}📈 Discriminante (Δ):{Style.RESET_ALL}")
        print(f"   Δ = b² - 4ac")
        print(f"   Δ = ({self.b})² - 4·({self.a})·({self.c})")
        print(f"   Δ = {Fore.YELLOW}{self.delta}{Style.RESET_ALL}")
        
        # Resolve baseado no delta
        print(f"\n{Fore.MAGENTA}✨ Resultado:{Style.RESET_ALL}")
        
        if self.delta < 0:
            resultado = f"   {Fore.RED}⚠ A equação não possui raízes reais.{Style.RESET_ALL}"
            explicacao = f"   (Delta negativo indica raízes complexas)"
        
        elif self.delta == 0:
            x = -self.b / (2 * self.a)
            resultado = f"   {Fore.GREEN}✓ A equação possui uma única raiz real:{Style.RESET_ALL}"
            resultado += f"\n   x = {Fore.YELLOW}{x:.4f}{Style.RESET_ALL}"
            explicacao = f"   (Delta zero indica duas raízes iguais)"
        
        else:
            x1 = (-self.b + math.sqrt(self.delta)) / (2 * self.a)
            x2 = (-self.b - math.sqrt(self.delta)) / (2 * self.a)
            resultado = f"   {Fore.GREEN}✓ A equação possui duas raízes reais distintas:{Style.RESET_ALL}"
            resultado += f"\n   x₁ = {Fore.YELLOW}{x1:.4f}{Style.RESET_ALL}"
            resultado += f"\n   x₂ = {Fore.YELLOW}{x2:.4f}{Style.RESET_ALL}"
            explicacao = f"   (Delta positivo indica duas raízes diferentes)"
        
        print(resultado)
        print(f"   {Fore.CYAN}{explicacao}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        return resultado
    
    def formatar_equacao(self):
        """Formata a equação de forma legível"""
        eq = f"{self.a}x²"
        
        if self.b >= 0:
            eq += f" + {self.b}x"
        else:
            eq += f" - {abs(self.b)}x"
        
        if self.c >= 0:
            eq += f" + {self.c}"
        else:
            eq += f" - {abs(self.c)}"
        
        eq += " = 0"
        return eq
    
    def executar(self, equacao=None):
        """
        Executa a calculadora completa
        Retorna a string com o resultado ou mensagem de erro
        """
        self.mostrar_banner()
        
        if equacao is None:
            self.mostrar_instrucoes()
            equacao = input(f"{Fore.GREEN}Digite a equação: {Style.RESET_ALL}")
        
        coeficientes = self.extrair_coeficientes(equacao)
        
        if coeficientes is None:
            mensagem = f"\n{Fore.RED}❌ Formato inválido!{Style.RESET_ALL}"
            mensagem += f"\n{Fore.YELLOW}Certifique-se de escrever no formato: ax^2+bx+c=0{Style.RESET_ALL}\n"
            print(mensagem)
            return mensagem
        
        if self.a == 0:
            mensagem = f"\n{Fore.RED}❌ Isso não é uma equação do segundo grau!{Style.RESET_ALL}"
            mensagem += f"\n{Fore.YELLOW}O coeficiente 'a' deve ser diferente de zero.{Style.RESET_ALL}\n"
            print(mensagem)
            return mensagem
        
        return self.resolver()


def main():
    """Função principal"""
    calc = BhaskaraCalculator()
    calc.executar()
    
    # Opção para calcular outra equação
    while True:
        print(f"\n{Fore.CYAN}Deseja calcular outra equação? (s/n): {Style.RESET_ALL}", end="")
        opcao = input().lower()
        
        if opcao == 's':
            print()
            calc.executar()
        else:
            print(f"\n{Fore.GREEN}Até logo! 👋{Style.RESET_ALL}\n")
            break


if __name__ == "__main__":
    main()
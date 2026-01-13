import random
import colorama
from colorama import Fore, Style
from enum import IntEnum

colorama.init(autoreset=True)

class Jogada(IntEnum):
    """Enum para as jogadas possíveis"""
    PEDRA = 1
    PAPEL = 2
    TESOURA = 3

class JogoPedraPapelTesoura:
    """Jogo de Pedra, Papel e Tesoura com IA que aprende"""
    
    # ASCII Art das jogadas
    ARTE = {
        Jogada.PEDRA: """    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)""",
        
        Jogada.PAPEL: """     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)""",
        
        Jogada.TESOURA: """    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)"""
    }
    
    NOMES = {
        Jogada.PEDRA: "PEDRA 🪨",
        Jogada.PAPEL: "PAPEL 📄",
        Jogada.TESOURA: "TESOURA ✂️"
    }
    
    def __init__(self):
        self.pontos_jogador = 0
        self.pontos_maquina = 0
        self.historico_jogador = []
        self.rodadas = 0
    
    def banner(self):
        """Exibe o banner do jogo"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}    🎮 PEDRA, PAPEL E TESOURA")
        print(f"{Fore.MAGENTA}    🤖 Máquina com IA que aprende seus padrões!")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def mostrar_placar(self):
        """Mostra o placar atual"""
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 PLACAR - Rodada {self.rodadas}{Style.RESET_ALL}")
        print(f"   Você: {Fore.GREEN}{self.pontos_jogador}{Style.RESET_ALL} | "
              f"Máquina: {Fore.RED}{self.pontos_maquina}{Style.RESET_ALL}")
        
        if len(self.historico_jogador) >= 3:
            print(f"{Fore.MAGENTA}🧠 A IA está analisando seu padrão de jogo...{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
    
    def solicitar_jogada(self):
        """
        Solicita a jogada do jogador
        
        Returns:
            Jogada ou None se quiser sair
        """
        print(f"{Fore.GREEN}Escolha sua jogada:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}1{Style.RESET_ALL} - 🪨 PEDRA")
        print(f"  {Fore.YELLOW}2{Style.RESET_ALL} - 📄 PAPEL")
        print(f"  {Fore.YELLOW}3{Style.RESET_ALL} - ✂️  TESOURA")
        print(f"  {Fore.RED}0{Style.RESET_ALL} - Sair")
        
        escolha = input(f"\nSua escolha: ").strip()
        
        if escolha == '0':
            return None
        
        if escolha not in ['1', '2', '3']:
            print(f"{Fore.RED}❌ Escolha inválida!{Style.RESET_ALL}")
            return None
        
        return Jogada(int(escolha))
    
    def ia_maquina(self):
        """
        IA que aprende padrões do jogador
        
        Returns:
            Jogada: Jogada escolhida pela máquina
        """
        # Nos primeiros 2 turnos, joga aleatório
        if len(self.historico_jogador) < 3:
            return Jogada(random.randint(1, 3))
        
        # Analisa frequência de jogadas
        pedra = self.historico_jogador.count(Jogada.PEDRA)
        papel = self.historico_jogador.count(Jogada.PAPEL)
        tesoura = self.historico_jogador.count(Jogada.TESOURA)
        
        # Analisa sequências (últimas 3 jogadas)
        ultimas_3 = self.historico_jogador[-3:]
        
        # Se o jogador está repetindo muito a mesma jogada
        if ultimas_3.count(ultimas_3[-1]) == 3:
            jogada_provavel = ultimas_3[-1]
        # Prediz baseado na jogada mais frequente
        elif pedra >= papel and pedra >= tesoura:
            jogada_provavel = Jogada.PEDRA
        elif papel >= pedra and papel >= tesoura:
            jogada_provavel = Jogada.PAPEL
        else:
            jogada_provavel = Jogada.TESOURA
        
        # Escolhe a jogada que vence a predição
        vence = {
            Jogada.PEDRA: Jogada.PAPEL,
            Jogada.PAPEL: Jogada.TESOURA,
            Jogada.TESOURA: Jogada.PEDRA
        }
        
        # 80% das vezes usa a IA, 20% joga aleatório para não ser previsível
        if random.random() < 0.8:
            return vence[jogada_provavel]
        else:
            return Jogada(random.randint(1, 3))
    
    def mostrar_jogada(self, jogada, jogador="Você"):
        """Mostra a arte ASCII da jogada"""
        cor = Fore.GREEN if jogador == "Você" else Fore.RED
        print(f"\n{cor}{jogador} escolheu: {self.NOMES[jogada]}{Style.RESET_ALL}")
        print(f"{cor}{self.ARTE[jogada]}{Style.RESET_ALL}")
    
    def determinar_vencedor(self, jogador, maquina):
        """
        Determina o vencedor da rodada
        
        Returns:
            str: 'jogador', 'maquina' ou 'empate'
        """
        if jogador == maquina:
            return 'empate'
        
        vitorias = {
            (Jogada.PEDRA, Jogada.TESOURA),
            (Jogada.PAPEL, Jogada.PEDRA),
            (Jogada.TESOURA, Jogada.PAPEL)
        }
        
        if (jogador, maquina) in vitorias:
            return 'jogador'
        else:
            return 'maquina'
    
    def mostrar_resultado(self, resultado):
        """Mostra o resultado da rodada"""
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        
        if resultado == 'empate':
            print(f"{Fore.YELLOW}🤝 EMPATE!{Style.RESET_ALL}")
        elif resultado == 'jogador':
            print(f"{Fore.GREEN}🎉 VOCÊ GANHOU!{Style.RESET_ALL}")
            self.pontos_jogador += 1
        else:
            print(f"{Fore.RED}😅 VOCÊ PERDEU!{Style.RESET_ALL}")
            self.pontos_maquina += 1
        
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do jogo"""
        print(f"\n{Fore.MAGENTA}📈 ESTATÍSTICAS DO JOGO:{Style.RESET_ALL}")
        print(f"   Total de rodadas: {self.rodadas}")
        
        if self.rodadas > 0:
            taxa_vitoria = (self.pontos_jogador / self.rodadas) * 100
            print(f"   Taxa de vitória: {taxa_vitoria:.1f}%")
        
        if len(self.historico_jogador) >= 3:
            pedra = self.historico_jogador.count(Jogada.PEDRA)
            papel = self.historico_jogador.count(Jogada.PAPEL)
            tesoura = self.historico_jogador.count(Jogada.TESOURA)
            
            print(f"\n   {Fore.CYAN}Suas jogadas:{Style.RESET_ALL}")
            print(f"   🪨 Pedra: {pedra} ({pedra/len(self.historico_jogador)*100:.1f}%)")
            print(f"   📄 Papel: {papel} ({papel/len(self.historico_jogador)*100:.1f}%)")
            print(f"   ✂️  Tesoura: {tesoura} ({tesoura/len(self.historico_jogador)*100:.1f}%)")
    
    def jogar_rodada(self):
        """Executa uma rodada do jogo"""
        self.rodadas += 1
        self.mostrar_placar()
        
        # Jogada do jogador
        jogada_jogador = self.solicitar_jogada()
        
        if jogada_jogador is None:
            return False  # Sinaliza para sair
        
        # Adiciona ao histórico
        self.historico_jogador.append(jogada_jogador)
        
        # Jogada da máquina
        jogada_maquina = self.ia_maquina()
        
        # Mostra as jogadas
        self.mostrar_jogada(jogada_jogador, "Você")
        self.mostrar_jogada(jogada_maquina, "Máquina")
        
        # Determina e mostra o vencedor
        resultado = self.determinar_vencedor(jogada_jogador, jogada_maquina)
        self.mostrar_resultado(resultado)
        
        return True  # Continua jogando
    
    def resetar(self):
        """Reseta o jogo"""
        self.pontos_jogador = 0
        self.pontos_maquina = 0
        self.historico_jogador = []
        self.rodadas = 0
        print(f"\n{Fore.YELLOW}🔄 Jogo resetado!{Style.RESET_ALL}")
    
    def jogar(self):
        """Loop principal do jogo"""
        self.banner()
        
        while True:
            continuar = self.jogar_rodada()
            
            if not continuar:
                break
            
            # Pergunta se quer continuar
            print(f"\n{Fore.CYAN}Jogar novamente? (s/n/r para resetar): {Style.RESET_ALL}", end="")
            resposta = input().strip().lower()
            
            if resposta == 'r':
                self.resetar()
            elif resposta != 's':
                break
        
        # Mostra estatísticas finais
        if self.rodadas > 0:
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}🏆 FIM DO JOGO!{Style.RESET_ALL}")
            print(f"\n   Placar Final:")
            print(f"   Você: {Fore.GREEN}{self.pontos_jogador}{Style.RESET_ALL} | "
                  f"Máquina: {Fore.RED}{self.pontos_maquina}{Style.RESET_ALL}")
            
            if self.pontos_jogador > self.pontos_maquina:
                print(f"\n   {Fore.GREEN}🎉 VOCÊ VENCEU O JOGO!{Style.RESET_ALL}")
            elif self.pontos_maquina > self.pontos_jogador:
                print(f"\n   {Fore.RED}😅 A MÁQUINA VENCEU!{Style.RESET_ALL}")
            else:
                print(f"\n   {Fore.YELLOW}🤝 EMPATE GERAL!{Style.RESET_ALL}")
            
            self.mostrar_estatisticas()
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Até logo! 👋{Style.RESET_ALL}\n")


def main():
    """Função principal"""
    jogo = JogoPedraPapelTesoura()
    jogo.jogar()


if __name__ == "__main__":
    main()
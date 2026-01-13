import pygame
import time
import os
from pathlib import Path
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class MusicPlayer:
    """Player de música simples usando pygame"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.musica_atual = None
        self.tocando = False
    
    def banner(self):
        """Exibe o banner do player"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}    🎵 MUSIC PLAYER")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    def verificar_arquivo(self, caminho):
        """
        Verifica se o arquivo de música existe
        
        Args:
            caminho (str): Caminho do arquivo
            
        Returns:
            bool: True se existe, False caso contrário
        """
        if not os.path.exists(caminho):
            print(f"{Fore.RED}❌ Erro: Arquivo '{caminho}' não encontrado!{Style.RESET_ALL}")
            return False
        
        extensoes_validas = ['.mp3', '.wav', '.ogg', '.flac']
        extensao = Path(caminho).suffix.lower()
        
        if extensao not in extensoes_validas:
            print(f"{Fore.RED}❌ Erro: Formato '{extensao}' não suportado!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Formatos aceitos: {', '.join(extensoes_validas)}{Style.RESET_ALL}")
            return False
        
        return True
    
    def carregar_musica(self, caminho):
        """
        Carrega um arquivo de música
        
        Args:
            caminho (str): Caminho do arquivo de música
            
        Returns:
            bool: True se carregou com sucesso, False caso contrário
        """
        if not self.verificar_arquivo(caminho):
            return False
        
        try:
            pygame.mixer.music.load(caminho)
            self.musica_atual = Path(caminho).name
            print(f"{Fore.GREEN}✓ Música carregada: {self.musica_atual}{Style.RESET_ALL}")
            return True
        except pygame.error as e:
            print(f"{Fore.RED}❌ Erro ao carregar música: {e}{Style.RESET_ALL}")
            return False
    
    def tocar(self, loops=0, inicio=0.0):
        """
        Toca a música carregada
        
        Args:
            loops (int): Número de repetições (-1 para infinito, 0 para tocar uma vez)
            inicio (float): Posição inicial em segundos
        """
        if self.musica_atual is None:
            print(f"{Fore.RED}❌ Nenhuma música carregada!{Style.RESET_ALL}")
            return False
        
        try:
            pygame.mixer.music.play(loops=loops, start=inicio)
            self.tocando = True
            print(f"{Fore.GREEN}▶️  Tocando: {self.musica_atual}{Style.RESET_ALL}")
            return True
        except pygame.error as e:
            print(f"{Fore.RED}❌ Erro ao tocar música: {e}{Style.RESET_ALL}")
            return False
    
    def pausar(self):
        """Pausa a música"""
        if self.tocando:
            pygame.mixer.music.pause()
            print(f"{Fore.YELLOW}⏸️  Música pausada{Style.RESET_ALL}")
    
    def retomar(self):
        """Retoma a música pausada"""
        pygame.mixer.music.unpause()
        print(f"{Fore.GREEN}▶️  Música retomada{Style.RESET_ALL}")
    
    def parar(self):
        """Para a música"""
        pygame.mixer.music.stop()
        self.tocando = False
        print(f"{Fore.RED}⏹️  Música parada{Style.RESET_ALL}")
    
    def ajustar_volume(self, volume):
        """
        Ajusta o volume da música
        
        Args:
            volume (float): Volume entre 0.0 e 1.0
        """
        volume = max(0.0, min(1.0, volume))  # Garante que está entre 0 e 1
        pygame.mixer.music.set_volume(volume)
        print(f"{Fore.CYAN}🔊 Volume ajustado para: {int(volume * 100)}%{Style.RESET_ALL}")
    
    def esta_tocando(self):

        return pygame.mixer.music.get_busy()
    
    def aguardar_fim(self, mostrar_progresso=True):

        if mostrar_progresso:
            print(f"{Fore.CYAN}Tocando", end="", flush=True)
        
        while self.esta_tocando():
            if mostrar_progresso:
                print(".", end="", flush=True)
            time.sleep(1)
        
        if mostrar_progresso:
            print(f" {Fore.GREEN}✓ Concluído!{Style.RESET_ALL}")
    
    def tocar_e_aguardar(self, caminho, volume=1.0):

        if self.carregar_musica(caminho):
            self.ajustar_volume(volume)
            if self.tocar():
                self.aguardar_fim()
    
    def listar_musicas_pasta(self, pasta="."):

        extensoes = ['.mp3', '.wav', '.ogg', '.flac']
        musicas = []
        
        try:
            for arquivo in Path(pasta).iterdir():
                if arquivo.suffix.lower() in extensoes:
                    musicas.append(str(arquivo))
            
            if musicas:
                print(f"\n{Fore.MAGENTA}🎵 Músicas encontradas:{Style.RESET_ALL}")
                for i, musica in enumerate(musicas, 1):
                    print(f"  {i}. {Path(musica).name}")
                print()
            else:
                print(f"{Fore.YELLOW}⚠️  Nenhuma música encontrada em '{pasta}'{Style.RESET_ALL}")
            
            return musicas
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao listar músicas: {e}{Style.RESET_ALL}")
            return []
    
    def fechar(self):
        """Encerra o pygame"""
        pygame.mixer.quit()
        pygame.quit()


def main():
    """Função principal com menu interativo"""
    player = MusicPlayer()
    player.banner()
    
    # Tenta tocar bluesky.mp3 se existir
    if os.path.exists("bluesky.mp3"):
        print(f"{Fore.GREEN}🎵 Encontrado: bluesky.mp3{Style.RESET_ALL}")
        player.tocar_e_aguardar("bluesky.mp3")
    else:
        print(f"{Fore.YELLOW}⚠️  bluesky.mp3 não encontrado{Style.RESET_ALL}\n")
        
        # Lista músicas disponíveis
        musicas = player.listar_musicas_pasta()
        
        if musicas:
            print(f"{Fore.CYAN}Digite o número da música para tocar (ou 'q' para sair): {Style.RESET_ALL}", end="")
            escolha = input()
            
            if escolha.lower() != 'q' and escolha.isdigit():
                idx = int(escolha) - 1
                if 0 <= idx < len(musicas):
                    player.tocar_e_aguardar(musicas[idx])
        else:
            print(f"{Fore.YELLOW}Adicione arquivos de música (.mp3, .wav, .ogg) nesta pasta{Style.RESET_ALL}")
    
    player.fechar()
    print(f"\n{Fore.GREEN}Até logo! 👋{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
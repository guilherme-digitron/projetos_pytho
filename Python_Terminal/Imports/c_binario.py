import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class ConversorBinario:
    """Conversor entre Decimal e Binário com explicação passo a passo"""
    
    def __init__(self):
        pass
    
    def banner(self):
        """Exibe o banner do conversor"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}     CONVERSOR DECIMAL BINÁRIO")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def menu(self):
        """
        Mostra o menu de opções
        
        Returns:
            int: Opção escolhida (1, 2 ou 0)
        """
        print(f"Escolha uma opção:")
        print(f"  {Fore.YELLOW}1{Style.RESET_ALL} - Decimal → Binário")
        print(f"  {Fore.YELLOW}2{Style.RESET_ALL} - Binário → Decimal")
        print(f"  {Fore.RED}0{Style.RESET_ALL} - Sair")
        
        try:
            opcao = int(input(f"\nSua escolha: "))
            return opcao
        except ValueError:
            print(f"{Fore.RED}❌ Entrada inválida!{Style.RESET_ALL}")
            return -1
    
    def decimal_para_binario(self, decimal, mostrar_passos=True):
        """
        Converte decimal para binário usando divisões sucessivas
        
        Args:
            decimal (int): Número decimal
            mostrar_passos (bool): Se deve mostrar o processo
            
        Returns:
            str: Número binário
        """
        if decimal == 0:
            return "0"
        
        if decimal < 0:
            print(f"{Fore.RED}⚠️  Número negativo! Convertendo valor absoluto.{Style.RESET_ALL}")
            decimal = abs(decimal)
        
        # Encontra as potências de 2 menores ou iguais ao número
        potencias = []
        potencia = 1
        
        while potencia <= decimal:
            potencias.append(potencia)
            potencia *= 2
        
        if mostrar_passos:
            print(f"\n{Fore.MAGENTA}📊 Processo de Conversão:{Style.RESET_ALL}")
            print(f"   Decimal: {Fore.YELLOW}{decimal}{Style.RESET_ALL}")
            print(f"   Potências de 2: {potencias}\n")
        
        # Constrói o binário
        binario = ""
        valor_restante = decimal
        
        for potencia in reversed(potencias):
            if valor_restante >= potencia:
                binario += "1"
                valor_restante -= potencia
                
                if mostrar_passos:
                    print(f"   {decimal} ≥ {potencia:>4} → bit 1 (resta {valor_restante})")
            else:
                binario += "0"
                
                if mostrar_passos:
                    print(f"   {decimal} < {potencia:>4} → bit 0")
        
        return binario
    
    def binario_para_decimal(self, binario, mostrar_passos=True):
        """
        Converte binário para decimal
        
        Args:
            binario (str): Número binário (string)
            mostrar_passos (bool): Se deve mostrar o processo
            
        Returns:
            int: Número decimal
        """
        # Valida se é binário
        if not all(bit in '01' for bit in binario):
            raise ValueError("O número deve conter apenas 0s e 1s!")
        
        decimal = 0
        tamanho = len(binario)
        
        if mostrar_passos:
            print(f"\n{Fore.MAGENTA}📊 Processo de Conversão:{Style.RESET_ALL}")
            print(f"   Binário: {Fore.YELLOW}{binario}{Style.RESET_ALL}\n")
        
        # Calcula o decimal
        for i, bit in enumerate(binario):
            posicao = tamanho - i - 1
            potencia = 2 ** posicao
            
            if bit == '1':
                decimal += potencia
                
                if mostrar_passos:
                    print(f"   Posição {posicao}: {bit} × 2^{posicao} = {bit} × {potencia:>4} = {potencia:>4}")
        
        if mostrar_passos:
            print(f"\n   {Fore.CYAN}Soma total: {Fore.YELLOW}{decimal}{Style.RESET_ALL}")
        
        return decimal
    
    def formatar_resultado(self, original, convertido, tipo_conversao):
        """Formata e exibe o resultado"""
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ RESULTADO:{Style.RESET_ALL}")
        
        if tipo_conversao == "decimal_binario":
            print(f"   Decimal:  {Fore.YELLOW}{original}{Style.RESET_ALL}")
            print(f"   Binário:  {Fore.GREEN}{convertido}{Style.RESET_ALL}")
            print(f"   Bits:     {len(convertido)}")
            
            # Mostra agrupado em bytes
            if len(convertido) > 4:
                agrupado = ' '.join([convertido[i:i+4] for i in range(0, len(convertido), 4)])
                print(f"   Agrupado: {Fore.CYAN}{agrupado}{Style.RESET_ALL}")
        
        else:  # binario_decimal
            print(f"   Binário:  {Fore.YELLOW}{original}{Style.RESET_ALL}")
            print(f"   Decimal:  {Fore.GREEN}{convertido}{Style.RESET_ALL}")
            print(f"   Bits:     {len(original)}")
        
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    
    def executar_decimal_binario(self):
        """Executa conversão Decimal → Binário"""
        try:
            valor = int(input(f"\n{Fore.GREEN}Digite o número decimal: {Style.RESET_ALL}"))
            binario = self.decimal_para_binario(valor)
            self.formatar_resultado(valor, binario, "decimal_binario")
            return True
        except ValueError as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}")
            return False
    
    def executar_binario_decimal(self):
        """Executa conversão Binário → Decimal"""
        try:
            binario = input(f"\n{Fore.GREEN}Digite o número binário: {Style.RESET_ALL}").strip()
            decimal = self.binario_para_decimal(binario)
            self.formatar_resultado(binario, decimal, "binario_decimal")
            return True
        except ValueError as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}")
            return False
    
    def mostrar_exemplos(self):
        """Mostra alguns exemplos de conversão"""
        print(f"\n{Fore.MAGENTA}💡 EXEMPLOS:{Style.RESET_ALL}\n")
        
        exemplos = [
            (10, "Decimal → Binário"),
            ("1010", "Binário → Decimal"),
            (255, "Decimal → Binário"),
            ("11111111", "Binário → Decimal")
        ]
        
        for valor, tipo in exemplos:
            if isinstance(valor, int):
                binario = self.decimal_para_binario(valor, mostrar_passos=False)
                print(f"   {valor:>3} (decimal) = {Fore.CYAN}{binario}{Style.RESET_ALL} (binário)")
            else:
                decimal = self.binario_para_decimal(valor, mostrar_passos=False)
                print(f"   {valor:>8} (binário) = {Fore.CYAN}{decimal}{Style.RESET_ALL} (decimal)")
    
    def executar(self):
        """Loop principal do programa"""
        self.banner()
        self.mostrar_exemplos()
        
        while True:
            print()
            opcao = self.menu()
            
            if opcao == 0:
                print(f"\n{Fore.GREEN}Até logo! 👋{Style.RESET_ALL}\n")
                break
            
            elif opcao == 1:
                self.executar_decimal_binario()
            
            elif opcao == 2:
                self.executar_binario_decimal()
            
            else:
                print(f"{Fore.RED}❌ Opção inválida! Escolha 0, 1 ou 2.{Style.RESET_ALL}")
            
            # Pergunta se quer continuar
            print(f"\n{Fore.CYAN}Pressione ENTER para continuar...{Style.RESET_ALL}", end="")
            input()


def main():
    """Função principal"""
    conversor = ConversorBinario()
    conversor.executar()


if __name__ == "__main__":
    main()
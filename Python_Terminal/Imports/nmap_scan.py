# nmap_terminal.py
# Programa simples para rodar Nmap pelo terminal em Python
# Funciona no Windows (incluindo Win7), Linux e macOS (se Nmap instalado)

import nmap

def print_header():
    print("\n" + "="*60)
    print("        NMAP SCANNER via Python Terminal")
    print("        (precisa ter Nmap instalado no sistema)")
    print("="*60 + "\n")

def menu():
    print_header()
    print("1. Scan simples de portas (top 1000)")
    print("2. Scan de versão + SO ( -sV -O )")
    print("3. Scan agressivo ( -A )")
    print("4. Scan rápido de rede (ex: 192.168.1.0/24)")
    print("5. Scan custom (você digita os argumentos)")
    print("6. Sair")
    print("-"*50)
    escolha = input("Digite o número da opção: ").strip()
    return escolha

def get_target():
    alvo = input("\nDigite o alvo (IP, hostname, faixa ex: 192.168.1.1 ou 192.168.1.0/24): ").strip()
    if not alvo:
        print("Alvo não informado. Usando localhost (127.0.0.1)")
        return "127.0.0.1"
    return alvo

def run_scan(alvo, argumentos):
    try:
        nm = nmap.PortScanner()
        print(f"\nExecutando: nmap {argumentos} {alvo}")
        print("-"*60)
        
        # Forma correta: hosts separado + arguments só com flags
        nm.scan(hosts=alvo, arguments=argumentos)
        
        print("\nResultados:")
        print("-"*60)
        
        for host in nm.all_hosts():
            print(f"Host : {host} ({nm[host].hostname() or 'sem hostname'})")
            print(f"Estado : {nm[host].state()}")
            
            for proto in nm[host].all_protocols():
                print(f"Protocolo : {proto}")
                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    info = nm[host][proto][port]
                    print(f"  Porta {port:5} | Estado: {info['state']:8} | Serviço: {info.get('name', '?')}")
            
            # Detecção de SO (se -O foi usado)
            if 'osmatch' in nm[host]:
                print("\nDetecção de SO:")
                for osm in nm[host]['osmatch']:
                    print(f"  {osm['name']} ({osm['accuracy']}%)")
        
        print("\nScan concluído.")
    
    except AttributeError as e:
        print("\nERRO: Biblioteca python-nmap não instalada corretamente ou conflito.")
        print("Tente: pip uninstall nmap && pip install python-nmap")
        print(f"Detalhe: {e}")
    except Exception as e:
        print(f"Erro inesperado: {type(e).__name__} → {e}")
    
    except nmap.PortScannerError as e:
        print("\nERRO: Não foi possível executar o Nmap.")
        print("Possíveis causas:")
        print("1. Nmap não está instalado")
        print("2. Nmap não está no PATH do sistema")
        print("3. Permissões insuficientes (tente rodar como administrador)")
        print(f"Detalhe: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def main():
    while True:
        op = menu()
        
        if op == "1":
            alvo = get_target()
            argumentos = "-sS -T4"               # SYN scan rápido
            run_scan(alvo, argumentos)

        elif op == "2":
            alvo = get_target()
            argumentos = "-sV -O -T4"            # versão + detecção de SO
            run_scan(alvo, argumentos)

        elif op == "3":
            alvo = get_target()
            argumentos = "-A -T4"                # agressivo completo
            run_scan(alvo, argumentos)

        elif op == "4":
            alvo = input("\nDigite a rede (ex: 192.168.1.0/24): ").strip() or "192.168.1.0/24"
            argumentos = "-sn"                   # ping scan (descobre hosts vivos)
            run_scan(alvo, argumentos)

        elif op == "5":
            full_cmd = input("\nDigite o comando completo após 'nmap ' (ex: -sV -p- 10.0.0.1): ").strip()
            if full_cmd:
                # Para scan custom: tenta separar o alvo do resto (simples)
                partes = full_cmd.split()
                alvo_custom = partes[-1] if partes else "127.0.0.1"
                argumentos_custom = ' '.join(partes[:-1]) if len(partes) > 1 else full_cmd
                run_scan(alvo_custom, argumentos_custom)
            else:
                print("Nenhum comando informado.")
                
                input("\nPressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {e}")
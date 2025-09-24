import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr = subprocess.STDOUT)
    return output.decode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(

        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''exemplo:
        netcat.py -t 192.168.1.108 -p 5555 -l -c # shell de comando
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # fazer upload de arquivo
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #executar comando

        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #enviar texto para porta 135 do servidor

        necat.py -t 192.168.1.108 -p 5555 #conectar ao servidor
        '''))

    parser.add_argument('-c', '--command', action='store_true', help='shell de comando')
    parser.add_argument('-e', '--execute', help='executar comando especificado')
    parser.add_argument('-l', '--listen', action='store_true', help='ouvir')
    
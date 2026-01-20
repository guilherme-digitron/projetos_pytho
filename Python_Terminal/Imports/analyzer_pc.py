import psutil
from colorama import init, Fore, Style

init(autoreset=True)

def show_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    print(Fore.GREEN + f"CPU Usage: {cpu_percent}%")
    if cpu_freq:
        print(Fore.GREEN + f"CPU Frequency: {cpu_freq.current} MHz")
    print(Fore.GREEN + f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical")

def show_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    print(Fore.BLUE + f"Memory Total: {memory.total / (1024 ** 3):.2f} GB")
    print(Fore.BLUE + f"Memory Used: {memory.used / (1024 ** 3):.2f} GB")
    print(Fore.BLUE + f"Memory Available: {memory.available / (1024 ** 3):.2f} GB")
    print(Fore.BLUE + f"Swap Total: {swap.total / (1024 ** 3):.2f} GB")
    print(Fore.BLUE + f"Swap Used: {swap.used / (1024 ** 3):.2f} GB")

def show_disk_info():
    disk = psutil.disk_usage('/')
    print(Fore.YELLOW + f"Disk Total: {disk.total / (1024 ** 3):.2f} GB")
    print(Fore.YELLOW + f"Disk Used: {disk.used / (1024 ** 3):.2f} GB")
    print(Fore.YELLOW + f"Disk Free: {disk.free / (1024 ** 3):.2f} GB")
    print(Fore.YELLOW + f"Disk Usage: {disk.percent}%")

def show_network_info():
    net_io = psutil.net_io_counters()
    print(Fore.MAGENTA + f"Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB")
    print(Fore.MAGENTA + f"Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")

def main():
    while True:
        print(Fore.CYAN + "Menu:")
        print(Fore.CYAN + "1. CPU Info")
        print(Fore.CYAN + "2. Memory Info")
        print(Fore.CYAN + "3. Disk Info")
        print(Fore.CYAN + "4. Network Info")
        print(Fore.CYAN + "5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            show_cpu_info()
        elif choice == '2':
            show_memory_info()
        elif choice == '3':
            show_disk_info()
        elif choice == '4':
            show_network_info()
        elif choice == '5':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

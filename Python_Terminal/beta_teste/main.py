import psutil
print(psutil.net_connections(kind='inet'))
for i in psutil.net_connections(kind='inet'):
    print(f"\n{i}")
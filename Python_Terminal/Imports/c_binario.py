while True:

    metodo = int(input("Qual metodo voce deseja ? "))
    valor = int(input("Digite o valor: "))
    binario = ""
    decimal = 0
    ti = 1
    a = 0
    b = -(a)
    listb = []
    if metodo == 1:

        while ti < valor:
            listb.append(ti)
            ti = ti * 2

        for i in reversed(listb):
        
            if valor - i < 0:
                binario += "0"
            else:
                valor -= i
                binario += "1"
        print(binario)

    if metodo == 0:
        
        valor = str(valor)
        for i in valor:
            i = 1
            listb.append(ti)
            ti = ti*2

        for i in range(len(listb)):
            if valor[i] == "1":
                decimal += listb[-(i+1)] 
        print(decimal)

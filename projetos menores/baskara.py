import re
import math

def extrair_coeficientes(equacao):
    equacao = equacao.replace(" ", "").lower()
    
    padrao = r"([-+]?\d*)x\^2([-+]?\d*)x([-+]?\d*)=0"
    match = re.match(padrao, equacao)
    
    if not match:
        return None  
    
    a, b, c = match.groups()
    
   
    a = int(a) if a and a not in ["+", "-"] else int(a + "1") 
    b = int(b) if b else 0  
    c = int(c) if c else 0  
    return a, b, c

def calcular_bhaskara(a, b, c):
    delta = b**2 - 4*a*c 
    
    if delta < 0:
        return "A equação não possui raízes reais."
    elif delta == 0:
        x = -b / (2 * a)  # 
        
        return f"A equação possui uma única raiz real: x = {x:.2f}"
    else:
        x1 = (-b + math.sqrt(delta)) / (2 * a)  
        x2 = (-b - math.sqrt(delta)) / (2 * a)  
        return f"As raízes da equação são: x1 = {x1:.2f}, x2 = {x2:.2f}"


equacao = input("Digite a equação do segundo grau (ex: 2x^2-3x+1=0): ")


coeficientes = extrair_coeficientes(equacao)

if coeficientes:
    a, b, c = coeficientes
    if a == 0:
        print("Isso não é uma equação do segundo grau! O coeficiente 'a' deve ser diferente de zero.")
    else:
        resultado = calcular_bhaskara(a, b, c)
        print(resultado)
else:
    print("Formato inválido! Certifique-se de escrever no formato correto, como: 2x^2-3x+1=0")
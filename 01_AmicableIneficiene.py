# Exemplo de código ineficiente.
def sumDiv(n):
    sum = 0
    for i in range(1, n):
        if n % i == 0:
            sum += i
    return sum

for a in range(1, 10000):
    for b in range(1, 10000):
        if sumDiv(a) == b and sumDiv(b) == a and a != b:
            print(a, b)
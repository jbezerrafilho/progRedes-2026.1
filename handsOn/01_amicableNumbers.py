# Definição para números amigos
# Se sumdiv(a) == b e sumdiv(b) == a, a != a entao a e b são números amigos.

def sumDiv(n):
    sum = 1
    root = int(n**0.5)
    for i in range(2, root + 1):
        if n % i == 0:
            sum += i
            if i != n // i:
                sum += n // i
    return sum

sumAmicable = 0
for a in range(1, 10000):
   b = sumDiv(a)
   if sumDiv(b) == a and b > a:
        print(a, b)
        sumAmicable += a + b  

print("Soma dos números amigos menores que 10000:", sumAmicable)
# Exibir todos os números ímpares de 1 a 1000 que possuem no máximo 10 divisores.
def numdiv(n):
    count = 1
    for i in range(3, n + 1, 2):
        if n % i == 0:
            count += 1
    return count


for num in range (1, 1001, 2):
    if numdiv(num) <= 10:
        sum += 1
        print(num)

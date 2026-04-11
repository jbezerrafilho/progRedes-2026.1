try:
    ip = input('Digite um ip válido: ')
    cidr = int(input('Digite uma máscara /(2-32): '))

    lista_octetos = [int(o) for o in ip.split('.')]
    if len(lista_octetos) != 4 or any(o < 0 or o > 255 for o in lista_octetos):
        raise ValueError("IP fora das regras (0-255).")

    if cidr < 2 or cidr > 32:
        raise ValueError("Máscara deve estar entre 2 e 32.")

except ValueError as e:
    print(f"Erro de Entrada: {e}")
    print("Certifique-se de usar apenas números nos locais corretos.")
    exit()

ip_32bits = 0 
for octeto in lista_octetos:
    ip_32bits = (ip_32bits << 8) | octeto

def calcular_parametros_ip(ip, cidr):
    bits_host = 32 - cidr
    
    # Cálculos usando Bitwise 
    rede = ip >> bits_host << bits_host
    broadcast = ip | (1 << bits_host) - 1
    primeiro_h = rede | 1
    ultimo_h = broadcast & ~1
    hosts_disp = (1 << bits_host) - 2
    mascara = (0xFFFFFFFF << bits_host) & 0xFFFFFFFF
    
    return rede, mascara, primeiro_h, ultimo_h, broadcast, hosts_disp


def bin_ipDecimal(endereco):
    o1 = (endereco >> 24) & 0xFF
    o2 = (endereco >> 16) & 0xFF
    o3 = (endereco >> 8) & 0xFF
    o4 = (endereco) & 0xFF
    return (f"{o1}.{o2}.{o3}.{o4}")

rede, mascara, primeiro_h, ultimo_h, broadcast, hosts_disp = calcular_parametros_ip(ip_32bits, cidr)

net = bin_ipDecimal(rede)
gateway = bin_ipDecimal(primeiro_h)
last_ip = bin_ipDecimal(ultimo_h)
brcast = bin_ipDecimal(broadcast)
mask = bin_ipDecimal(mascara)


print(f"""
    {'Rede:':<20} {net:>15}
    {'Máscara:':<20} {mask:>15}
    {'Gateway:':<20} {gateway:>15}
    {'Último Host:':<20} {last_ip:>15}
    {'Host Disponíveis:':<20} {hosts_disp:>15}
    {'Broadcast:':<20} {brcast:>15}
""")

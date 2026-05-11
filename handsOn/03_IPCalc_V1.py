ip = input('Digite um ip válido: ')  #str
cidr = int(input('Digite uma máscara válida no formato /XX: ')) #int

lista_octetos = ip.split('.') #lista com str's
ip_semponto = 0 #int
for octeto in lista_octetos:
    ip_semponto = (ip_semponto << 8) | int(octeto)

def calcular_parametros_ip(ip, cidr):
    # 1. Preparação dos bits
    bits_host = 32 - cidr
    
    # 2. Cálculos usando Bitwise (A lógica que você criou)
    rede = ip >> bits_host << bits_host
    broadcast = ip | (1 << bits_host) - 1
    primeiro_h = rede | 1
    ultimo_h = broadcast & ~1
    hosts_disp = (1 << bits_host) - 2
    mascara = (0xFFFFFFFF << bits_host) & 0xFFFFFFFF
    
    # Retornamos os valores em ordem
    return rede, mascara, primeiro_h, ultimo_h, broadcast, hosts_disp


def bin_ipDecimal(endereco):
    o1 = (endereco >> 24) & 0xFF
    o2 = (endereco >> 16) & 0xFF
    o3 = (endereco >> 8) & 0xFF
    o4 = (endereco) & 0xFF
    return (f"{o1}.{o2}.{o3}.{o4}")

rede, mascara, primeiro_h, ultimo_h, broadcast, hosts_disp = calcular_parametros_ip(ip_semponto, cidr)

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

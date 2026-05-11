ip = input('Digite um ip válido: ')  #str
mask = int(input('Digite uma máscara válida no formato /XX: ')) #int

lista_octetos = ip.split('.') #lista com str's
ip_semponto = 0 #int
for octeto in lista_octetos:
    ip_semponto = (ip_semponto << 8) | int(octeto)

hosts = (32 - mask)  #int: Equivale aos bits disponíveis para hosts
rede = ip_semponto >> hosts << hosts #int, mas internamente o int é armazenado em bits

broadcast = ip_semponto | (1 << hosts) - 1 
#broadcast = rede + (2 ** hosts - 1)

primeiro_host = rede | 1
#primeiro_host = rede + 1

ultimo_host = broadcast & ~1
#ultimo_host = broadcast - 1

hosts_disponiveis = (1 << hosts) - 2 
#hosts_disponiveis = (2 ** hosts) - 2
mask_bin = (0xFFFFFFFF << hosts) & 0xFFFFFFFF


def bin_ipDecimal(endereco):
    o1 = (endereco >> 24) & 0xFF
    o2 = (endereco >> 16) & 0xFF
    o3 = (endereco >> 8) & 0xFF
    o4 = (endereco) & 0xFF
    return (f"{o1}.{o2}.{o3}.{o4}")

net = bin_ipDecimal(rede)
start_ip = bin_ipDecimal(primeiro_host)
last_ip = bin_ipDecimal(ultimo_host)
bc = bin_ipDecimal(broadcast)
mask_decimal = bin_ipDecimal(mask_bin)


print(f"""
    {'Rede:':<20} {net:>15}
    {'Máscara:':<20} {mask_decimal:>15}
    {'Gateway:':<20} {start_ip:>15}
    {'Último Host:':<20} {last_ip:>15}
    {'Host Disponíveis:':<20} {hosts_disponiveis:>15}
    {'Broadcast:':<20} {bc:>15}
""")

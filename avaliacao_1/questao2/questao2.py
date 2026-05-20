# 20242014050043 - José Bezerra Filho
# 20242014050014 - Israel Levi de Paiva Norato

import sys
import struct
import socket

if len(sys.argv) < 2:
    print('Uso: python questao2.py <arquivo.pcpa>')
    sys.exit()

arquivo = sys.argv[1]

try:
    arquivo = open(arquivo, 'rb')

except FileNotFoundError:
    print('Arquivo não encontrado!')
    sys.exit()

with arquivo as f: 

    # Cabeçalho do Arquivo PCAP
    file_header = f.read(24)  
    magic_number = int.from_bytes(file_header[:4], 'big')

    if magic_number in (0xA1B2C3D4, 0xD4C3B2A1):
        endian = 'big' if magic_number == 0xA1B2C3D4 else 'little'
        div_time = 1_000_000
    elif magic_number in (0xA1B23C4D, 0x4D3CB2A1):
        endian = 'big' if magic_number == 0xA1B23C4D else 'little'
        div_time = 1_000_000_000
    else:
        print('Arquivo Pcap inválido!')
        sys.exit()

    count = 0
    count_bytes_ip = {}
    time_init = 0
    time_end = 0

    while True: 
        # Cabeçalho do Pacote do Arquivo PCAP
        packet_header = f.read(16) 
        if len(packet_header) < 16:
            break
        count += 1

        tseg = int.from_bytes(packet_header[0:4], endian)
        tuseg = int.from_bytes(packet_header[4:8], endian)
        timestamp = tseg +  (tuseg / div_time) 
        if not time_init:
            time_init = timestamp
        time_end = timestamp

        packet_data_length = int.from_bytes(packet_header[8:12], endian)
        packet_data = f.read(packet_data_length) 
        if len(packet_data) < 14:
            continue

        # Camada 2 - Header do Enlace
        ether_header = packet_data[:14]
        dst_mac, src_mac, ether_type = struct.unpack('!6s6sH', ether_header)
        
        dst_mac = ':'.join(f'{b:02x}' for b in dst_mac)
        src_mac = ':'.join(f'{b:02x}' for b in src_mac)

        if ether_type != 0x800:
            continue

        if len(packet_data) < 34:
            continue

        # Camada 3 - Header do IP    
        ip_header = packet_data[14:34]
        version_ihl, total_len, ttl, protocol, src_ip, dst_ip = struct.unpack('!BxH4xBB2x4s4s', ip_header)   
        version_ip= version_ihl >> 4
        ihl = (version_ihl & 0x0F) * 4
        src_ip = socket.inet_ntoa(src_ip) 
        dst_ip = socket.inet_ntoa(dst_ip)   
        
        for ip in (src_ip, dst_ip):
            count_bytes_ip[ip] = count_bytes_ip.get(ip, 0) + total_len

        
        print(f'\nPacote número: {count}')
        print(f'MACs: dst {dst_mac} -> src {src_mac}')
        print(f'IPs: src {src_ip} -> dst {dst_ip}')
        print(f'Version: {version_ip}, IHL: {ihl}, TTL: {ttl}, Protocolo: {protocol}')

        
        ip_payload = packet_data[14 + ihl:]
        # Apesar de encapsulado pelo IP, mas ainda na camada 3 (particularidade ICMP)
        if protocol == 1:
            if len(ip_payload) < 4:
                continue
            icmp_type = ip_payload[0]
            icmp_code = ip_payload[1]
            
            icmp_types = {
                0: 'Echo Reply',
                3: 'Destination Unreachable',
                5: 'Redirect',
                8: 'Echo Request',
                11: 'Time Exceeded',
            }

            tipo = icmp_types.get(icmp_type, f'Tipo {icmp_type}')
            print(f'ICMP: Tipo {tipo}')
                    
            if icmp_type in (0, 8):
                ident = int.from_bytes(ip_payload[4:6], 'big')
                seq = int.from_bytes(ip_payload[6:8], 'big')
                print(f'Identificação: {ident} - Sequência: {seq}')
        # Camada 4 - TCP        
        elif protocol == 6:
            if len(ip_payload) < 20:
                continue

            src_p, dst_p, seq, ack, off_flags, win = struct.unpack('!HHIIHH', ip_payload[0:16])
            flags = off_flags & 0x3F
            tipos_flags = {
                1: 'FIN',
                2: 'SYN',
                4: 'RST',
                8: 'PSH',
                16: 'ACK',
                32: 'URG'
            }
            flags_ativas = [nome for bit, nome in tipos_flags.items() if flags & bit]

            print(f'TCP: src Port {src_p}, dst Port {dst_p} | Seq {seq}, ACK {ack}')
            print(f'Flags: {flags_ativas}, Window Size: {win}')
        # Camada 4 - UDP    
        elif protocol == 17:
            if len(ip_payload) < 8:
                continue
            src_p, dst_p = struct.unpack('!HH', ip_payload[0:4])
            print(f'UDP: src Port {src_p}, dst Port {dst_p}')

    if count_bytes_ip:
        ip_captura = max(count_bytes_ip, key=lambda ip : count_bytes_ip[ip])
        del count_bytes_ip[ip_captura]
        if count_bytes_ip:
            ip_winner = max(count_bytes_ip, key=lambda ip : count_bytes_ip[ip])
            ip_winner_bytes = count_bytes_ip[ip_winner]
            megabytes = ip_winner_bytes / (1024 ** 2) 
            print(f'\nO ip que mais trocou dados foi: {ip_winner} com {megabytes:.2f}MB!')
        else: 
            print("\nApenas um IP foi detectado na captura.")
    intervalo = time_end - time_init
    print(f'O intervalo de captura do pacote foi de {intervalo:.6f}s!\n')
           

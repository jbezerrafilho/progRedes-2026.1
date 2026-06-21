import socket
import struct

CLIENT_FILES = "client_files/"
SERVER = ("127.0.0.1", 12346)
ERRO = b"ERRO"
CHUNK = b"CHUNK"

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.settimeout(2.0)

while True:
    file_name = input("Nome do arquivo a baixar: ")
    my_sock.sendto(file_name.encode(), SERVER)

    data, _ = my_sock.recvfrom(2048)
    pedacos = {}
    total = 0
    transferencia_ok = True

    if data.startswith(ERRO):
        print(data[4:].decode())
        continue

    while data.startswith(CHUNK):
        idx, total = struct.unpack("!II", data[5:13])
        conteudo = data[13:]
        pedacos[idx] = conteudo
        print(f"Recebido pedaço {idx + 1} de {total}")

        if len(pedacos) == total:
            break
        try:
            data, _ = my_sock.recvfrom(2048)
        except TimeoutError:
            print(f"Timeout — recebidos {len(pedacos)} de {total} pedaços. Descartando.")
            transferencia_ok = False
            break

    if not transferencia_ok:
        continue
    conteudo_final = b"".join(pedacos[i] for i in range(total))

    with open(CLIENT_FILES + file_name, "wb") as fd:
        fd.write(conteudo_final)

    print(f"Arquivo {file_name} recebido com sucesso!")

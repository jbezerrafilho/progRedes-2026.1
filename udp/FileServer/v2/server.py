import socket
import struct
import time

SERVER_FILES = "server_files/"
ERRO = b"ERRO"
CHUNK = b"CHUNK"
CHUNK_SIZE = 1024

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind(("127.0.0.1", 12346))

while True:
    file_name, source = my_sock.recvfrom(512)

    try:
        with open(SERVER_FILES + file_name.decode(), "rb") as fd:
            data = fd.read()
    except FileNotFoundError:
        msg = f"Arquivo {file_name.decode()} não encontrado!"
        my_sock.sendto(ERRO + msg.encode(), source)
        continue

    pedacos = [data[i : i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    total = len(pedacos)
    print(f"Enviando {file_name.decode()} em {total} fragmento(s).")

    for idx, pedaco in enumerate(pedacos):
        header = b"CHUNK" + struct.pack("!II", idx, total)
        my_sock.sendto(header + pedaco, source)
        time.sleep(0.001)
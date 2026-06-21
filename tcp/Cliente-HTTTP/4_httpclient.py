import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_chunks(body):
    data = b""
    pos = 0
    while True:
        fim = body.find(b'\r\n', pos)
        tam = int(body[pos:fim], 16)
        inicio_chunk = fim + 2
        fim_chunk = fim + 2 + tam
        if tam == 0:
            break
        data += body[inicio_chunk:fim_chunk]
        pos = fim + 2 + tam + 2
    return data

def get_data(url, resource, output):
    s.connect((url, 80))
    s.send(("GET " + resource + " HTTP/1.1\r\n"
    "Host: " + url + "\r\n" 
    "Connection: close\r\n"
    "\r\n").encode())

    data_raw = b""

    while True:
        block = s.recv(4096)
        if not block:
            break
        data_raw += block
    header, body = data_raw.split(b'\r\n\r\n', 1)
    print(header.decode())

    if b"Transfer-Encoding" in header:
        body = get_chunks(body)

    with open(output, 'wb') as fd:
        fd.write(body)

if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("Uso: python script url resource output")
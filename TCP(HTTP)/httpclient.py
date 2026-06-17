import socket
import sys

B2NL = b"\r\n\r\n"
BNL = b"\r\n"

def get_chunk(data, sock, output):
    with open(output, "wb") as fd:
        while True:
            posLN = data.find(BNL)
            chunk_len = int(data[:posLN], 16)
            data = data[posLN + 2:]

            if chunk_len == 0:
                break
            
            while len(data) < chunk_len + 2:
                data += sock.recv(4096)

            fd.write(data[:chunk_len])
            data = data[chunk_len + 2:]

    print("Recurso salvo com sucesso!!")

def save_data(data, length, sock, output):
    with open(output, "wb") as fd:
        fd.write(data)
        received = len(data)
        while received < length:
            data = sock.recv(4096)
            if not data:
                break
            fd.write(data)
            received += len(data)
    print("Arquivo salvo com sucesso!")

def get_data(url, resource, output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url, 80))
    
    sock.send(("GET " + resource + " HTTP/1.1\r\n" +
               "Host: " + url + "\r\n" +
               "\r\n").encode())
               
    data = sock.recv(4096)

    pos2NL = data.find(B2NL)
    headers = data[:pos2NL].decode().upper().split("\r\n")
    data = data[pos2NL + 4:] 

    for header in headers:
        header = header.split(":", 1)
        if "CONTENT-LENGTH" in header:
            contentLEN = int(header[1])
            print(f"Iniciando donwload - tamanho: {contentLEN} Bytes!")
            save_data(data, contentLEN, sock, output)
            break
        if"TRANSFER-ENCODING" in header:
            print("Transferindo em blocos...")
            get_chunk(data, sock, output)
            break
    sock.close()       

if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print(
        "Uso: python hc.py url resource output\n"
        "Ex:  python hc.py httpbin.org /image/png porco.png \n"
        "Ex:  python hc.py httpbin.org /image/jpeg lobo.jpg \n"
        "Ex:  python hc.py viacep.com.br /ws/59062570/json/ meucep.json \n"
    )
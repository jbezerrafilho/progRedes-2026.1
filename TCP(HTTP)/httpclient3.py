import socket
import sys

def get_data(site, resource, output):
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect((site, 80))

    my_sock.send(("GET " + resource + " HTTP/1.1\r\n"
                "Host: " + site + "\r\n"
                "\r\n").encode())

    data = b""
    while b"\r\n\r\n" not in data: 
        data += my_sock.recv(4096)

    pos2NL = data.find(b"\r\n\r\n")
    headers = data[:pos2NL].split(b'\r\n')

    for header in headers:
        print(header.decode())

    len_body = -1
    for header in headers[1:]:
        header = header.split(b':')
        if header[0] == b'Content-Length':
            len_body = int(header[1])

    if len_body != -1:
        body = data[pos2NL+4:]
        while len(body) < len_body:
            body += my_sock.recv(4096)
        my_sock.close()
        fd = open(output, "wb")
        fd.write(body)
        fd.close()
    else:
        print("Content=Lenght não encontrado!")
        my_sock.close()

if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print ("uso: python site resource output_filename")
    print ("Exemplos:")
    print (" python httpclient3.py httpbin.org /image/png porco.png")
    print (" python httpclient3.py viacep.com.br /ws/59062570/json/ meucep.json")
    print (" python httpclient3.py httpbin.org /image/jpeg lobo.jpg")
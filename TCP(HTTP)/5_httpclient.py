import sys
import socket

def get_chunks(ini_body, sock, fd):
    data = ini_body
    pos = 0
    while True:
        fim = data.find(b"\r\n", pos)
        tam = int(data[pos:fim], 16)
        ini_chunk = fim + 2
        fim_chunk = fim + 2 + tam
        if tam == 0:
            break
        fd.write(data[ini_chunk:fim_chunk])
        data += sock.recv(4096)
        pos = fim + 2 + tam + 2
    print('Recurso consumido com sucesso!')

def get_data(site, resource, output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((site, 80))

    sock.send (("GET "+resource+" HTTP/1.1\r\n"+
                   "Host: "+site+"\r\n"+
                   "\r\n").encode())

    data_raw = sock.recv(4096)
    pos2NL = data_raw.find(b"\r\n\r\n")
    headers = data_raw[:pos2NL].split(b'\r\n')

    len_data = -1
    for header in headers[1:]:
        header = header.split(b":")
        if b"Content-Length" in header:
            len_data = int(header[1])
            
    with open(output, 'wb') as fd:
        if len_data != -1:
            print (f"tamanho dos dados: {len_data}")
            ini_body = data_raw[pos2NL + 4] 
            fd.write(ini_body) 
            t_body = len(ini_body)
            while len(t_body) < len_data:
                block = sock.recv(4096)
                fd.write(block) 
                t_body += len(block)       
        else:
            ini_body = data_raw[pos2NL + 4:]
            get_chunks(ini_body, sock, fd)


if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print ("uso: python site resource output_filename")
    print ("Exemplos:")
    print (" python httpclient3.py httpbin.org /image/png porco.png ")
    print (" python httpclient3.py viacep.com.br /ws/59062570/json/ meucep.json ")
    print (" python httpclient3.py httpbin.org /image/jpeg lobo.jpg ")
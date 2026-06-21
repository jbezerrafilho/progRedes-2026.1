import sys
import socket

def get_chunks(ini_body, sock, fd):
    buffer = ini_body
    
    while True:
        fim_linha_tam = buffer.find(b"\r\n")
       
        if fim_linha_tam == -1:
            block = sock.recv(4096)
            if not block:
                print("Conexão fechada prematuramente pelo servidor.")
                break
            buffer += block
            continue
            
        try:
            tam_chunk = int(buffer[:fim_linha_tam], 16)
        except ValueError:
            print("Erro ao decodificar o tamanho do chunk.")
            break
            
        if tam_chunk == 0:
            print('Recurso chunked consumido com sucesso!')
            break
    
        tam_total_necessario = fim_linha_tam + 2 + tam_chunk + 2
        
        if len(buffer) < tam_total_necessario:
            bloco = sock.recv(4096)
            if not bloco:
                print("Conexão interrompida antes do fim do chunk.")
                break
            buffer += bloco
            continue
            
        ini_dados = fim_linha_tam + 2
        fim_dados = ini_dados + tam_chunk
        dados_puros = buffer[ini_dados:fim_dados]
        fd.write(dados_puros)
    
        buffer = buffer[tam_total_necessario:]

def get_data(site, resource, output):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((site, 80))

    sock.send(("GET " + resource + " HTTP/1.1\r\n" +
               "Host: " + site + "\r\n" +
               "Connection: close\r\n\r\n").encode())

    data_raw = sock.recv(4096)
    pos2NL = data_raw.find(b"\r\n\r\n")
    if pos2NL == -1:
        print("Erro: Cabeçalho HTTP inválido ou incompleto.")
        return
        
    headers = data_raw[:pos2NL].split(b'\r\n')

    len_data = -1
    for header in headers[1:]:
        if b":" in header:
            chave, valor = header.split(b":", 1)
            if b"content-length" in chave.lower():
                len_data = int(valor.strip())
            
    with open(output, 'wb') as fd:
        if len_data != -1:
            print(f"tamanho dos dados (Content-Length): {len_data}")
            ini_body = data_raw[pos2NL + 4:] 
            fd.write(ini_body) 
            
            bytes_baixados = len(ini_body)
            while bytes_baixados < len_data:
                block = sock.recv(4096)
                if not block:
                    break
                fd.write(block) 
                bytes_baixados += len(block)       
            print("Recurso salvo com sucesso!")
        else:
            print("Detectado Transfer-Encoding: chunked. Processando blocos...")
            ini_body = data_raw[pos2NL + 4:]
            get_chunks(ini_body, sock, fd)
            
    sock.close()

if len(sys.argv) == 4:
    get_data(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("uso: python site resource output_filename")
    print (" python httpclient.py httpbin.org /image/png porco.png ")
    print (" python httpclient.py viacep.com.br /ws/59062570/json/ meucep.json ")
    print (" python httpclient.py httpbin.org /image/jpeg lobo.jpg ")
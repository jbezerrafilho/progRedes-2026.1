import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try: 
    while True:
        msg = input('Digite sua mensagem: ').encode()
        if msg: 
            sender = s.sendto(msg,('127.0.0.1', 5000) )
            print(f'Enviado {sender} bytes')  
            data, source =  s.recvfrom(1024)
            print(f'Recebido de volta a mensagem: {data.decode()}')
        else:
            break
except KeyboardInterrupt:
    print('\nEncerrado pelo CMD')

s.close()

  



import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5000))
print('Escutando em localhost:5000')

while True:
  data, source =  s.recvfrom(1024)
  qtd_b = s.sendto(data, source)
  print(f'Recebido {qtd_b} bytes')






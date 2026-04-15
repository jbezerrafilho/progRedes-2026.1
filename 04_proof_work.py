import hashlib
import time

def minerar(texto, bits_0):
    texto_bytes = texto.encode('UTF-8')
    nonce = 0
     
    inicio = time.perf_counter()

    while True:
        nonce_bytes = nonce.to_bytes(4, 'big')
        dados_concatenados = nonce_bytes + texto_bytes
        hash = hashlib.sha256(dados_concatenados).digest()
        valor_hash = int.from_bytes(hash, 'big')
        bits_iniciais = valor_hash >> (256 - bits_0)
        if bits_iniciais == 0:
            fim = time.perf_counter()
            tempo_total = fim -inicio
            print(f' O hash encontrado foi: {hash.hex()}')
            print(f' Tempo gasto: {tempo_total:.4f} segundos')
            return nonce
        nonce += 1
       


texto = input('Digite uma string de entrada: ')
zeros = int(input('Digite a quantidade de bits 0: '))

nonce = minerar(texto, zeros)
print(f" O nonce que satisfaz a condição é: {nonce}")   
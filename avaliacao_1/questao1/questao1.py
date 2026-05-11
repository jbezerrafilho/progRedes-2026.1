# 20242014050043 - José Bezerra Filho 
import sys
import subprocess
import os
import struct

        
def jpeg_valido(caminho):
    with open(caminho, 'rb') as f:
        if not f.read(2) == b'\xff\xd8':
            return False
        return True

def extrair_gps(caminho):
    with open(caminho, 'rb') as f:
        pos = f.seek(2)
        ident = f.read(2)
        if ident != b'\xff\xe1':
            pos = int.from_bytes(f.read(2), 'big')
            f.seek(pos - 2, 1)
            ident = f.read(2)
        #print(ident)
        f.seek(8, 1)
        endian = f.read(2)
        order = 'big' if endian == b'MM' else 'little'
        f.seek(6, 1)
        qt_meta = int.from_bytes(f.read(2))
        print(f.read(2))
        # for _ in range(qt_meta):
        #     print(f.read(2))
        
        

if len(sys.argv) < 2:
    print('Uso: python.py <diretório>')
    sys.exit()

cam_dir = sys.argv[1]
if not os.path.isdir(cam_dir):
    print('Diretório inválido')
    sys.exit()

comando = ['cmd', '/c', 'dir', '/b', cam_dir]
conteudo_dir = subprocess.check_output(comando, text=True)
org_dir = conteudo_dir.splitlines()

#print(org_dir)
fotos = []


for nome_foto in org_dir:
    full_path = os.path.join(cam_dir, nome_foto)
    if not jpeg_valido(full_path):
        continue
    fotos.append(nome_foto)
    gps = extrair_gps(full_path)


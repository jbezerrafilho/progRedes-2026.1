import os

BLOCK_SIZE = 64536

def cypher_block(block, key, start):
    output = bytearray(len(block))
    len_key = len(key)
    for index in range(len(block)):
        output[index] = block[index] ^ key[start]
        start = (start + 1) % len_key        
    return start, output

def cypher_file(file_name, key):
    old_file_name = f"{file_name}.bak"
    try:
        os.remove(old_file_name)
    except FileNotFoundError:
        None
    os.rename (file_name, old_file_name)

    try:  
        with open(file_name, "wb") as out, open(old_file_name, "rb") as inp:
            start = 0
            key = key.encode('utf-8')
            block = inp.read(BLOCK_SIZE)
            while block:
                start, cyphered = cypher_block(block, key, start)
                out.write(cyphered)
                block = inp.read(BLOCK_SIZE)
    except FileNotFoundError as fnf:
        print (f"Arquivo nao encontrado: {fnf.filename}")            
        
def main(file_name, key):
    cypher_file(file_name, key)
    
if __name__ == "__main__":
    main(input("Digite o nome do arquivo a cifrar: "),
         input("Digite a palavra chave: "))
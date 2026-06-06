import base64
import os

separador = lambda titulo: print(f"\n{'='*50}\n{titulo}\n{'='*50}")
separador("EXP 1 — Cadeia completa: bit → ASCII → Base64")

texto = "Hi"
print(f"Texto Original: {texto!r}")

# Byte brutos
raw = texto.encode("ascii")
print(f"Bytes : {list(raw)}")

# Representação binária
bits = " ".join(f"{byte:08b}" for byte in raw)
print(f"Bits: {bits}")

# Base64
encoded = base64.b64encode(raw)
print(encoded)
print(encoded.decode())

separador("EXP 2 — Overhead de 33%")

dados = os.urandom(1000)           # 1000 bytes aleatórios (simula binário)
encoded = base64.b64encode(dados)

original  = len(dados)
codificado = len(encoded)
overhead  = (codificado - original) / original * 100

print(f"Tamanho original  : {original} bytes")
print(f"Tamanho em Base64 : {codificado} bytes")
print(f"Overhead          : {overhead:.1f}%")

separador("EXP 3 — Bytes de controle vs Base64")

print("Bytes brutos:")
# 0x0A = '\n' (quebra de linha), 0x00 = null byte
bytes_problematicos = bytes([72, 101, 108, 0x0A, 108, 111, 0x00, 33])
nomes = {0x0A: "← QUEBRA DE LINHA!", 0x00: "← NULL BYTE!"}

for b in bytes_problematicos:
    nome = nomes.get(b, "")
    print(f"  {b:3d}  {b:08b}  {nome}")

print("\nEm Base64 (todos os chars são seguros):")
print(" ", base64.b64encode(bytes_problematicos).decode())
print("  → nenhum caractere de controle no resultado")


separador("EXP 4 — Base64 não é criptografia")

segredo = "senha_super_secreta_123"
falsa_segurança = base64.b64encode(segredo.encode()).decode()

print(f"String original : {segredo!r}")
print(f"Em Base64       : {falsa_segurança!r}")
print(f"Decodificado    : {base64.b64decode(falsa_segurança).decode()!r}")
print("\n⚠  Qualquer pessoa decodifica em 1 linha. Não é criptografia.")

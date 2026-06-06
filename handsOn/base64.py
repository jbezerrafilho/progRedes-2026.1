import base64
import os

# ============================================================
# LAB BASE64 — do bit ao protocolo
# ============================================================

separador = lambda titulo: print(f"\n{'='*50}\n{titulo}\n{'='*50}")


# ────────────────────────────────────────────────
# EXP 1 — A cadeia completa: bit → ASCII → Base64
# ────────────────────────────────────────────────
separador("EXP 1 — Cadeia completa: bit → ASCII → Base64")

texto = "Hi"
print(f"Texto original : {texto!r}")

# Bytes brutos
raw = texto.encode("ascii")
print(f"Bytes (decimal): {list(raw)}")

# Representação binária — o nível elétrico
bits = " ".join(f"{byte:08b}" for byte in raw)
print(f"Bits           : {bits}")

# Base64
encoded = base64.b64encode(raw)
print(f"Base64         : {encoded.decode()}")

# Decodificando de volta
decoded = base64.b64decode(encoded)
print(f"Decodificado   : {decoded.decode()}")


# ────────────────────────────────────────────────
# EXP 2 — O overhead de 33%
# ────────────────────────────────────────────────
separador("EXP 2 — Overhead de 33%")

dados = os.urandom(1000)           # 1000 bytes aleatórios (simula binário)
encoded = base64.b64encode(dados)

original  = len(dados)
codificado = len(encoded)
overhead  = (codificado - original) / original * 100

print(f"Tamanho original  : {original} bytes")
print(f"Tamanho em Base64 : {codificado} bytes")
print(f"Overhead          : {overhead:.1f}%")


# ────────────────────────────────────────────────
# EXP 3 — O problema que o Base64 resolve:
#          bytes de controle corrompem texto
# ────────────────────────────────────────────────
separador("EXP 3 — Bytes de controle vs Base64")

# 0x0A = '\n' (quebra de linha), 0x00 = null byte
bytes_problematicos = bytes([72, 101, 108, 0x0A, 108, 111, 0x00, 33])

print("Bytes brutos:")
for b in bytes_problematicos:
    nome = {0x0A: "← QUEBRA DE LINHA!", 0x00: "← NULL BYTE!"}.get(b, "")
    print(f"  {b:3d}  {b:08b}  {nome}")

print("\nEm Base64 (todos os chars são seguros):")
print(" ", base64.b64encode(bytes_problematicos).decode())
print("  → nenhum caractere de controle no resultado")


# ────────────────────────────────────────────────
# EXP 4 — Base64 NÃO é criptografia
# ────────────────────────────────────────────────
separador("EXP 4 — Base64 não é criptografia")

segredo = "senha_super_secreta_123"
falsa_segurança = base64.b64encode(segredo.encode()).decode()

print(f"String original : {segredo!r}")
print(f"Em Base64       : {falsa_segurança!r}")
print(f"Decodificado    : {base64.b64decode(falsa_segurança).decode()!r}")
print("\n⚠  Qualquer pessoa decodifica em 1 linha. Não é criptografia.")


# ────────────────────────────────────────────────
# EXP 5 — Imagem → Base64 → Data URL (HTML)
#          simulando o que um navegador faz
# ────────────────────────────────────────────────
separador("EXP 5 — Imagem em Base64 embutida em HTML")

# Cria um PNG mínimo válido (1x1 pixel vermelho)
# Bytes reais de um PNG — isso é binário puro
png_1x1 = bytes([
    0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A,  # assinatura PNG
    0x00,0x00,0x00,0x0D,0x49,0x48,0x44,0x52,  # chunk IHDR
    0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x01,
    0x08,0x02,0x00,0x00,0x00,0x90,0x77,0x53,
    0xDE,0x00,0x00,0x00,0x0C,0x49,0x44,0x41,  # chunk IDAT
    0x54,0x08,0xD7,0x63,0xF8,0xCF,0xC0,0x00,
    0x00,0x00,0x02,0x00,0x01,0xE2,0x21,0xBC,
    0x33,0x00,0x00,0x00,0x00,0x49,0x45,0x4E,  # chunk IEND
    0x44,0xAE,0x42,0x60,0x82
])

img_b64 = base64.b64encode(png_1x1).decode()
data_url = f"data:image/png;base64,{img_b64}"

html = f"""<!DOCTYPE html>
<html>
<body>
  <!-- imagem sem nenhum arquivo externo, tudo embutido em Base64 -->
  <img src="{data_url}" width="100" height="100"
       style="image-rendering:pixelated">
  <p>Tamanho do PNG original : {len(png_1x1)} bytes</p>
  <p>Tamanho em Base64       : {len(img_b64)} bytes</p>
</body>
</html>"""

with open("lab_base64.html", "w") as f:
    f.write(html)

print(f"PNG original      : {len(png_1x1)} bytes")
print(f"Base64 da imagem  : {img_b64}")
print(f"\nArquivo gerado    : lab_base64.html")
print("Abra no navegador — a imagem está 100% embutida, sem arquivo externo.")
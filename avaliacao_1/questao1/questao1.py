# 20242014050043 - José Bezerra Filho
# 20242014050014 - Israel Levi de Paiva Norato
import sys
import os
import struct


def jpeg_valido(caminho):
    with open(caminho, "rb") as f:
        return f.read(2) == b"\xff\xd8"


def ler_racional(dados, endian, offset):
    numerador = struct.unpack(endian + "I", dados[offset : offset + 4])[0]
    denominador = struct.unpack(endian + "I", dados[offset + 4 : offset + 8])[0]
    return numerador / denominador if denominador != 0 else 0


def ler_coordenada(dados, endian, inicio_tiff, valor):
    offset = struct.unpack(endian + "I", valor)[0]
    pos_racionais = inicio_tiff + offset
    g = ler_racional(dados, endian, pos_racionais)
    m = ler_racional(dados, endian, pos_racionais + 8)
    s = ler_racional(dados, endian, pos_racionais + 16)
    return g + (m / 60) + (s / 3600)


def extrair_gps(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()

    # localiza o bloco EXIF
    pos_exif = dados.find(b"Exif\x00\x00")
    if pos_exif == -1:
        return None

    inicio_tiff = pos_exif + 6
    endian = "<" if dados[inicio_tiff : inicio_tiff + 2] == b"II" else ">"

    # navega até o IFD0 e procura a tag GPS (0x8825)
    offset_ifd0 = struct.unpack(
        endian + "I", dados[inicio_tiff + 4 : inicio_tiff + 8]
    )[0]
    pos_ifd0 = inicio_tiff + offset_ifd0
    total_entradas = struct.unpack(
        endian + "H", dados[pos_ifd0 : pos_ifd0 + 2]
    )[0]

    cursor = pos_ifd0 + 2
    pos_ifd_gps = None
    for _ in range(total_entradas):
        tag = struct.unpack(endian + "H", dados[cursor : cursor + 2])[0]
        if tag == 0x8825:
            offset_gps = struct.unpack(
                endian + "I", dados[cursor + 8 : cursor + 12]
            )[0]
            pos_ifd_gps = inicio_tiff + offset_gps
            break
        cursor += 12

    if pos_ifd_gps is None:
        return None

    # lê as tags de latitude e longitude
    total_tags_gps = struct.unpack(
        endian + "H", dados[pos_ifd_gps : pos_ifd_gps + 2]
    )[0]
    cursor = pos_ifd_gps + 2

    lat = lon = ref_lat = ref_lon = None
    for _ in range(total_tags_gps):
        tag = struct.unpack(endian + "H", dados[cursor : cursor + 2])[0]
        valor = dados[cursor + 8 : cursor + 12]

        if tag == 1:
            ref_lat = valor[:1]
        elif tag == 2:
            lat = ler_coordenada(dados, endian, inicio_tiff, valor)
        elif tag == 3:
            ref_lon = valor[:1]
        elif tag == 4:
            lon = ler_coordenada(dados, endian, inicio_tiff, valor)

        cursor += 12

    if lat is None or lon is None:
        return None

    if ref_lat == b"S":
        lat = -lat
    if ref_lon == b"W":
        lon = -lon

    return lat, lon


def listar_arquivos(diretorio):
    return [
        nome for nome in os.listdir(diretorio)
        if os.path.isfile(os.path.join(diretorio, nome))
    ]


def processar_fotos(caminho):
    coords = []
    for arquivo in listar_arquivos(caminho):
        full_path = os.path.join(caminho, arquivo)

        try:
            if not jpeg_valido(full_path):
                continue
        except Exception:
            continue

        gps = extrair_gps(full_path)
        if gps is None:
            print(f"{arquivo}: sem GPS")
            continue

        lat, lon = gps
        print(f"{arquivo}")
        print(f"Latitude : {lat}")
        print(f"Longitude: {lon}")
        print("-" * 40)

        coords.append(f"{lat:.5f},{lon:.5f}")
        if len(coords) == 10:
            break

    return coords


def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <diretório>")
        sys.exit(1)

    coords = processar_fotos(sys.argv[1])

    if coords:
        link = "https://www.google.com/maps/dir/" + "/".join(coords)
        print(f"\nRota no Google Maps:\n{link}\n")
    else:
        print("\nNenhuma foto com GPS encontrada.")


if __name__ == "__main__":
    main()
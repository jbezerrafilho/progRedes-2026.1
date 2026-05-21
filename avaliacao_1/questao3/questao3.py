# 20242014050043 - José Bezerra Filho
# 20242014050014 - Israel Levi de Paiva Norato
import os
import sys


raid = {
    "qtd_discos": 0,
    "tam_disco": 0,
    "tam_bloco": 0,
    "pasta": "",
    "discos_ausentes": []
}


def get_config():
    try:
        qtd_discos = int(input("Quantidade de discos [03 - mínimo]: "))
        tam_disco = int(input("Tamanho do disco em bytes: "))
        tam_bloco = int(input("Tamanho do bloco em bytes: "))
        pasta = input("Salvar no caminho: ").strip()
    except ValueError:
        print("Digite números inteiros onde solicitado")
        return None
    if qtd_discos < 3:
        print("Erro: RAID4 exige no mínimo 3 discos.")
        return None

    if tam_disco <= 0 or tam_bloco <= 0:
        print("Erro: tamanhos devem ser maiores que zero.")
        return None

    if tam_disco % tam_bloco != 0:
        print("Erro: o tamanho do disco deve ser múltiplo do bloco.")
        return None
    return (qtd_discos, tam_disco, tam_bloco, pasta)
    

def set_config(qtd_discos, tam_disco, tam_bloco, pasta):
    raid["qtd_discos"] = qtd_discos
    raid["tam_disco"] = tam_disco
    raid["tam_bloco"] = tam_bloco
    raid["pasta"] = pasta
    raid["discos_ausentes"] = []


def valida_posicao(pos_inicio, tam_dados):

    qtd_disc_dados = raid["qtd_discos"] - 1
    tam_logico = qtd_disc_dados * raid["tam_disco"]

    if not (0 <= pos_inicio < tam_logico):
        print("Erro: Posição fora do intervalo!")
        return False

    if pos_inicio + tam_dados > tam_logico:
        print("Erro: Dados ultrapassam o tamanho lógico.")
        return False

    return True


def get_disc_pos(cursor):

    tam_bloco = raid["tam_bloco"]
    qtd_discos_dados = raid["qtd_discos"] - 1

    bloco = cursor // tam_bloco
    disco = bloco % qtd_discos_dados
    linha = bloco // qtd_discos_dados
    offset = cursor % tam_bloco
    pos_f = (linha * tam_bloco) + offset

    return (disco, linha, offset, pos_f)


def set_paridade(linha):

    qtd_discos_dados = raid["qtd_discos"] - 1
    tam_bloco = raid["tam_bloco"]
    pasta = raid["pasta"]
    pos_bloco = linha * tam_bloco
    paridade = bytearray(tam_bloco)

    for i in range(qtd_discos_dados):

        if i in raid["discos_ausentes"]:
            continue

        caminho = os.path.join(pasta, f"disco{i}.bin")

        try:
            with open(caminho, "rb") as f:
                f.seek(pos_bloco)
                dados = f.read(tam_bloco)

            for j in range(len(dados)):
                paridade[j]  = paridade[j] ^ dados[j]

        except Exception as e:
            print(f"Erro ao ler disco{i}.bin para paridade: {e}")
            return

    idx_disco_par = raid["qtd_discos"] - 1

    if idx_disco_par in raid["discos_ausentes"]:
        print("Aviso: disco de paridade ausente — paridade não atualizada.")
        return

    caminho_par = os.path.join(pasta, f"disco{idx_disco_par}.bin")

    try:
        with open(caminho_par, "r+b") as f:
            f.seek(pos_bloco)
            f.write(bytes(paridade))

    except Exception as e:
        print(f"Erro ao escrever disco de paridade: {e}")


def inicializa_raid():

    print("\nIniciando Raid 4")
    config = get_config()
    if config is None:
        return
    
    qtd_discos, tam_disco, tam_bloco, pasta = config
    set_config(qtd_discos, tam_disco, tam_bloco, pasta)

    try:
        os.makedirs(pasta, exist_ok=True)
        print("pasta criada")
    except Exception as e:
        print(f"Erro ao criar pasta {e}")
        return
    qtd_discos_dados = qtd_discos - 1
    
    try:
        for i in range(qtd_discos_dados):
            caminho = os.path.join(pasta, f"disco{i}.bin")
            with open(caminho, "wb") as f:
                f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco de dados: {e}")

    try:
        idx_disco_par = qtd_discos - 1
        cam_disco_par = os.path.join(pasta, f"disco{idx_disco_par}.bin")
        with open(cam_disco_par, "wb") as f:
            f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco de paridade: {e}")

    print("\nRaid 4 iniciado com sucesso!\n"
      f"  Discos de dados  : {qtd_discos_dados} x {tam_disco} bytes\n"
      f"  Disco de paridade: 1 x {tam_disco} bytes\n"        
      f"  Capacidade lógica: {qtd_discos_dados * tam_disco} bytes\n"
      f"  Blocos por disco : {tam_disco // tam_bloco}\n")     


def obtem_raid():

    print("\n=== Obtendo INFOs do RAID 4 ===")
    config = get_config()
    if config is None:
        return
    
    qtd_discos, tam_disco, tam_bloco, pasta = config
    set_config(qtd_discos, tam_disco, tam_bloco, pasta)

    print("\nVerificando discos...")

    for i in range(qtd_discos):
        caminho = os.path.join(pasta, f"disco{i}.bin")
        tipo = "PARID" if i == (qtd_discos - 1) else "dados"

        if os.path.exists(caminho):
            tamanho_real = os.path.getsize(caminho)  

            if tamanho_real != tam_disco:           
                print(f"disco{i}.bin — tamanho incompatível!")
                print(f"  esperado  : {tam_disco} bytes")
                print(f"  encontrado: {tamanho_real} bytes")
                sys.exit(
                    "Erro: configuração incompatível com os arquivos."
                     " \U0001F6A8")

            print(f"disco{i}.bin - ({tipo}) {tamanho_real} bytes ✅")

        else:
            raid["discos_ausentes"].append(i)
            print(f"disco{i}.bin - ({tipo}) AUSENTE ❌")

    qtd_ausentes = len(raid["discos_ausentes"])

    if not raid["discos_ausentes"]:
        print("\nRaid 4 Saudável. Operando Normalmente!")
    elif qtd_ausentes == 1:
        print("\nRaid 4 Degradado!")
        idx_disco = raid["discos_ausentes"][0]
        tipo = "PARIDADE" if idx_disco == qtd_discos - 1 else "dados"
        print(f"Substitua o disco{idx_disco}.bin - {tipo}")
    else:
        sys.exit("\nErro fatal: Possível perda de DADOS!")


def escreve_raid():

    print("\n === Escrevendo no Raid 4 ===")
    tam_logico = raid["tam_disco"] * (raid["qtd_discos"] - 1)

    dados = input("Dados para gravar: ").encode("utf-8") 

    try:
        pos_inicio = int(input(f"Posicao Inicial [0 a {tam_logico - 1}]: "))
    except ValueError:
        print("Erro: A posicao deve ser um número inteiro.")
        return

    if not valida_posicao(pos_inicio, len(dados)):
        return

    cursor         = pos_inicio
    dados_a_gravar = dados
    tam_bloco      = raid["tam_bloco"]

    while dados_a_gravar:

        disco, linha, offset, pos_f = get_disc_pos(cursor)

        espaco_bloco              = tam_bloco - offset
        dados_permitidos_no_bloco = min(espaco_bloco, len(dados_a_gravar))
        fatia                     = dados_a_gravar[:dados_permitidos_no_bloco]

        if disco in raid["discos_ausentes"]:
            print(f"Disco{disco} Ausente")
        else:
            caminho = os.path.join(raid["pasta"], f"disco{disco}.bin")
            try:
                with open(caminho, "r+b") as f:
                    f.seek(pos_f)
                    f.write(fatia)
            except Exception as e:
                print(f"Erro ao escrever no disco{disco}.bin: {e}")
                return

        set_paridade(linha)
        dados_a_gravar = dados_a_gravar[dados_permitidos_no_bloco:]
        cursor        += dados_permitidos_no_bloco

    print(f"\n{len(dados)} bytes gravados a partir da posição {pos_inicio} [OK].")

def le_raid():

    print("\n === Lendo do Raid 4 ===")
    tam_bloco  = raid["tam_bloco"]
    tam_logico = raid["tam_disco"] * (raid["qtd_discos"] - 1)

    try:
        pos_inicio = int(input(f"Posição inicial [0 a {tam_logico - 1}]: "))
        qtd_bytes  = int(input("Quantos bytes ler: "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    if not valida_posicao(pos_inicio, qtd_bytes):
        return

    cursor = pos_inicio
    bytes_a_ler = qtd_bytes
    bytes_lidos  = bytearray()
    qtd_disc_dados = raid["qtd_discos"] - 1
    
    while bytes_a_ler:

        disco, _, offset, pos_f = get_disc_pos(cursor)
        espaco_bloco = tam_bloco - offset
        quanto_ler = min(espaco_bloco, bytes_a_ler)
       
        if disco not in raid["discos_ausentes"]:
            caminho = os.path.join(raid["pasta"], f"disco{disco}.bin")
            try:
                with open(caminho, "rb") as f:
                    f.seek(pos_f)
                    fatia = f.read(quanto_ler)
            except Exception as e:
                print(f"Erro ao ler disco{disco}.bin: {e}")
                return

        else:
            print(f"Disco{disco} ausente — reconstruindo via XOR...")

            idx_par = raid["qtd_discos"] - 1
            cam_par = os.path.join(raid["pasta"], f"disco{idx_par}.bin")

            try:
                with open(cam_par, "rb") as f:
                    f.seek(pos_f)
                    fatia = bytearray(f.read(quanto_ler))
            except Exception as e:
                print(f"Erro ao ler paridade: {e}")
                return
            
            for i in range(qtd_disc_dados):
                if i == disco:
                    continue
                caminho_i = os.path.join(raid["pasta"], f"disco{i}.bin")
                try:
                    with open(caminho_i, "rb") as f:
                        f.seek(pos_f)
                        dados_i = f.read(quanto_ler)

                    for j in range(len(dados_i)):
                        fatia[j] = fatia[j] ^ dados_i[j]

                except Exception as e:
                    print(f"Erro ao ler disco{i}.bin: {e}")
                    return

        bytes_lidos += fatia
        bytes_a_ler -= quanto_ler
        cursor += quanto_ler

    print(f"\n{len(bytes_lidos)} bytes lidos:")
    try:
        print(f"\U0001F4C4  {bytes_lidos.decode('utf-8')}")

    except UnicodeDecodeError:
        print("Texto: (dados binários)")

    input("\nPressione Enter para continuar...")


def remove_disco_raid():

    print("\n === Removendo Disco do Raid 4 ===")
    intervalo = raid["qtd_discos"] - 1

    try:
        disco = int(input(f"Índice do disco a remover (0 a {intervalo}): "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    if disco < 0 or disco >= raid["qtd_discos"]:
        print("Erro: índice de disco inválido.")
        return

    if disco in raid["discos_ausentes"]:
        print(f"Disco{disco}.bin já está ausente!")
        return

    if raid["discos_ausentes"]:
        print("Erro: já existe um disco ausente.")
        print("Remover outro tornaria o RAID irrecuperável.")
        return

    caminho = os.path.join(raid["pasta"], f"disco{disco}.bin")
    try:
        os.remove(caminho)
        print(f"disco{disco}.bin removido fisicamente.")
    except FileNotFoundError:
        print(f"Erro: disco{disco}.bin não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao remover disco{disco}.bin: {e}")
        return

    raid["discos_ausentes"].append(disco)

    print(f"\nRAID4 operando em modo DEGRADADO.")
    print(f"disco{disco}.bin ausente — leitura e escrita continuam normalmente.")
    print(f"Use reconstroi_raid() para recuperar o disco.")


def reconstroi_raid():

    print("\n === Reconstruindo Disco do Raid 4 ===")

    if not raid["discos_ausentes"]:
        print("Nenhum disco ausente. Reconstrução desnecessária.")
        return

    if len(raid["discos_ausentes"]) > 1:
        print("Erro: mais de um disco ausente. Impossível reconstruir.")
        return

    disco        = raid["discos_ausentes"][0]
    tam_bloco    = raid["tam_bloco"]
    tam_disco    = raid["tam_disco"]
    qtd_discos   = raid["qtd_discos"]  
    pasta        = raid["pasta"]
    total_blocos = tam_disco // tam_bloco

    print(f"Reconstruindo disco{disco}.bin...")

    caminho_novo = os.path.join(pasta, f"disco{disco}.bin")  
    try:
        with open(caminho_novo, "wb") as f:
            f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco{disco}.bin: {e}")
        return

    try:
        for bloco in range(total_blocos): 

            pos_bloco          = bloco * tam_bloco
            bloco_reconstruido = bytearray(tam_bloco)

            for i in range(qtd_discos):
                if i == disco:
                    continue

                caminho_i = os.path.join(pasta, f"disco{i}.bin") 
                with open(caminho_i, "rb") as f:
                    f.seek(pos_bloco)
                    bloco_i = f.read(tam_bloco) 

                for j in range(len(bloco_i)):
                    bloco_reconstruido[j] = bloco_reconstruido[j] ^ bloco_i[j]  

            with open(caminho_novo, "r+b") as f:  
                f.seek(pos_bloco)
                f.write(bytes(bloco_reconstruido))

            print(f"  bloco {bloco + 1}/{total_blocos} reconstruído...")

    except Exception as e:
        print(f"Erro durante a reconstrução: {e}")
        return

    raid["discos_ausentes"].remove(disco)

    print(f"\ndisco{disco}.bin reconstruído com sucesso!")
    print("RAID4 operando normalmente. \u2705")


def main():
    try:
        while True:
            print("\n=== SIMULADOR RAID 4 ===\n"
                  "1. Inicializar RAID\n"
                  "2. Obter RAID existente\n"
                  "3. Escrever no RAID\n"
                  "4. Ler do RAID\n"
                  "5. Remover Disco\n"
                  "6. Reconstruir Disco\n"
                  "7. Sair\n")
            try:
                opcao = int(input("Escolha uma opção: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continue

            if opcao == 1:
                inicializa_raid()
            elif opcao == 2:
                obtem_raid()
            elif opcao == 3:
                if raid["qtd_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    escreve_raid()
            elif opcao == 4:
                if raid["qtd_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    le_raid()
            elif opcao == 5:
                if raid["qtd_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    remove_disco_raid()
            elif opcao == 6:
                if raid["qtd_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    reconstroi_raid()
            elif opcao == 7:
                print("Saindo da simulação.\n")
                break
            else:
                print("Opção inválida!")

    except KeyboardInterrupt:
        sys.exit("\n\nSimulação encerrada pelo usuário. Até logo!\n")


if __name__ == "__main__":
    main()


# 20242014050043 - José Bezerra Filho
# 20242014050014 - Israel Levi de Paiva Norato

import os
import sys

raid = {
    "pasta": "",
    "num_discos": 0,
    "tam_disco": 0,
    "tam_bloco": 0,
    "discos_ausentes": [],
}

def get_config():

    try:
        num_discos = int(input("Quantidade de discos [03 - mínimo]: "))
        tam_disco = int(input("Tamanho do disco em bytes: "))
        tam_bloco = int(input("Tamanho do bloco em bytes: "))
        pasta = input("Salvar no caminho: ").strip()
        if num_discos < 3:
            print("Erro: RAID4 exige no mínimo 3 discos.")
            return None

        if tam_disco <= 0 or tam_bloco <= 0:
            print("Erro: tamanhos devem ser maiores que zero.")
            return None

        if tam_disco % tam_bloco != 0:
            print("Erro: o tamanho do disco deve ser múltiplo do bloco.")
            return None
        return (num_discos, tam_disco, tam_bloco, pasta)
    
    except ValueError:
        print("Digite números inteiros onde solicitado")
        return None

def set_config(num_discos, tam_disco, tam_bloco, pasta):

    raid["num_discos"] = num_discos
    raid["tam_disco"] = tam_disco
    raid["tam_bloco"] = tam_bloco
    raid["pasta"] = pasta
    raid["discos_ausentes"] = []

def get_disc_pos(pos_log):

    tam_bloco = raid["tam_bloco"]
    qtd_discos = raid["num_discos"] - 1

    bloco = pos_log // tam_bloco
    disco = bloco % qtd_discos
    linha = bloco // qtd_discos
    offset = pos_log % tam_bloco
    pos_f = (linha * tam_bloco) + offset

    return (disco, linha, offset, pos_f)

def set_paridade(linha):

    qtd_discos = raid["num_discos"] - 1
    tam_bloco = raid["tam_bloco"]
    pasta = raid["pasta"]
    pos_bloco = linha * tam_bloco
    paridade = bytearray(tam_bloco)

    for i in range(qtd_discos):

        if i in raid["discos_ausentes"]:
            continue

        caminho = os.path.join(pasta, f"disco{i}.bin")

        try:
            with open(caminho, "rb") as f:
                f.seek(pos_bloco)
                dados = f.read(tam_bloco)

            for j in range(len(dados)):
                paridade[j] ^= dados[j]

        except Exception as e:
            print(f"Erro ao ler disco{i}.bin para paridade: {e}")
            return

    idx_disco_par = raid["num_discos"] - 1

   
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

def valida_posicao(pos_inicio, tam_dados):

    qtd_disc_dados = raid["num_discos"] - 1
    tam_logico = qtd_disc_dados * raid["tam_disco"]

    if not (0 <= pos_inicio < tam_logico):
        print("Erro: Posição fora do intervalo!")
        return False

    if pos_inicio + tam_dados > tam_logico:
        print("Erro: Dados ultrapassam o tamanho lógico.")
        return False

    return True

def inicializa_raid():

    print("\nIniciando Raid 4")
    config = get_config()

    if config is None:
        return
    
    num_discos, tam_disco, tam_bloco, pasta = config
    set_config(num_discos, tam_disco, tam_bloco, pasta)

    try:
        os.makedirs(pasta, exist_ok=True)
        print("pasta criada")

    except Exception as e:
        print(f"Erro ao criar pasta {e}")

    num_discos_dados = num_discos - 1
    try:
        for i in range(num_discos_dados):
            caminho = os.path.join(pasta, f"disco{i}.bin")
            with open(caminho, "wb") as f:
                f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco de dados: {e}")

    try:
        idx_disco_par = num_discos - 1
        cam_disco_par = os.path.join(pasta, f"disco{idx_disco_par}.bin")
        with open(cam_disco_par, "wb") as f:
            f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco de paridade: {e}")

    print("\nRaid 4 iniciado com sucesso!\n"   
      f"  Discos: {num_discos_dados}\n"    
      f"  Capacidade: {num_discos_dados * tam_disco} bytes\n") 

def obtem_raid():

    print("\n=== Obtendo INFOs do RAID 4 ===")
    respostas = get_config()
    if respostas is None:
        return
    num_discos, tam_disco, tam_bloco, pasta = respostas
    set_config(num_discos, tam_disco, tam_bloco, pasta)

    print("\nVerificando discos...")

    for i in range(num_discos):
        caminho = os.path.join(pasta, f"disco{i}.bin")
        tipo = "PARID" if i == (num_discos - 1) else "dados"

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

    if qtd_ausentes == 0:
        print("\nRaid 4 Saudável. Operando Normalmente!")

    elif qtd_ausentes == 1:
        print("\nRaid 4 Degradado!")
        idx_disco = raid["discos_ausentes"][0]
        tipo = "PARIDADE" if idx_disco == num_discos - 1 else "dados"
        print(f"Substitua o disco{idx_disco}.bin - {tipo}")
    else:
        sys.exit("\nErro fatal: Possível perda de DADOS!")

def escreve_raid():

    print("\n === Escrevendo no Raid 4 ===")
    tam_bloco = raid["tam_bloco"]
    tam_logico = raid["tam_disco"] * (raid["num_discos"] - 1)

    try:
        dados = input("Dados para gravar: ").encode("utf-8")
        pos_inicio = int(input(f"Posicao Inicial [0 a {tam_logico - 1}]: "))

    except ValueError:
        print("Erro: A posicao deve ser um número inteiro.")
        return

    if not valida_posicao(pos_inicio, len(dados)):
        return

    pos_logica = pos_inicio
    dados_restantes = dados
    tam_bloco = raid["tam_bloco"]

    while len(dados_restantes) > 0:

        disco, linha, offset, pos_f = get_disc_pos(pos_logica)

        espaco_bloco = tam_bloco - offset
        qtd_escrever = min(espaco_bloco, len(dados_restantes))
        fatia = dados_restantes[:qtd_escrever]

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
        dados_restantes = dados_restantes[qtd_escrever:]
        pos_logica += qtd_escrever
    print(f"\n{len(dados)} bytes gravados a partir da posição {pos_inicio} [OK].")

def le_raid():

    print("\n === Lendo do Raid 4 ===")
    tam_bloco  = raid["tam_bloco"]
    tam_logico = raid["tam_disco"] * (raid["num_discos"] - 1)

    try:
        pos_inicio = int(input(f"Posição inicial [0 a {tam_logico - 1}]: "))
        qtd_bytes  = int(input("Quantos bytes ler: "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    if not valida_posicao(pos_inicio, qtd_bytes):
        return

    pos_logica   = pos_inicio
    bytes_faltam = qtd_bytes
    dados_lidos  = bytearray()

    while bytes_faltam > 0:

        disco, linha, offset, pos_f = get_disc_pos(pos_logica)

        espaco_no_bloco = tam_bloco - offset
        qtd_ler         = min(espaco_no_bloco, bytes_faltam)

        if disco not in raid["discos_ausentes"]:
            caminho = os.path.join(raid["pasta"], f"disco{disco}.bin")
            try:
                with open(caminho, "rb") as f:
                    f.seek(pos_f)
                    fatia = f.read(qtd_ler)
            except Exception as e:
                print(f"Erro ao ler disco{disco}.bin: {e}")
                return

        else:
            print(f"Disco{disco} ausente — reconstruindo via XOR...")

            idx_par   = raid["num_discos"] - 1
            cam_par   = os.path.join(raid["pasta"], f"disco{idx_par}.bin")
            pos_bloco = linha * raid["tam_bloco"]

            try:
                with open(cam_par, "rb") as f:
                    f.seek(pos_bloco + offset)
                    fatia = bytearray(f.read(qtd_ler))
            except Exception as e:
                print(f"Erro ao ler paridade: {e}")
                return

            qtd_disc_dados = raid["num_discos"] - 1
            for i in range(qtd_disc_dados):
                if i == disco:
                    continue
                if i in raid["discos_ausentes"]:
                    continue

                cam_i = os.path.join(raid["pasta"], f"disco{i}.bin")
                try:
                    with open(cam_i, "rb") as f:
                        f.seek(pos_bloco + offset)
                        dados_i = f.read(qtd_ler)

                    for j in range(len(dados_i)):
                        fatia[j] ^= dados_i[j]

                except Exception as e:
                    print(f"Erro ao ler disco{i}.bin: {e}")
                    return

        dados_lidos  += fatia
        bytes_faltam -= qtd_ler
        pos_logica   += qtd_ler

    print(f"\n{len(dados_lidos)} bytes lidos:")
    try:
        print(f"\U0001F4C4  {dados_lidos.decode("utf-8")}")

    except UnicodeDecodeError:
        print("Texto: (dados binários)")

    input("\nPressione Enter para continuar...")

def remove_disco_raid():

    print("\n === Removendo Disco do Raid 4 ===")

    try:
        intervalo = raid["num_discos"] - 1
        disco = int(input(f"Índice do disco a remover (0 a {intervalo}): "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    if disco < 0 or disco >= raid["num_discos"]:
        print("Erro: índice de disco inválido.")
        return

    if disco in raid["discos_ausentes"]:
        print(f"Disco{disco}.bin já está ausente!")
        return

    if len(raid["discos_ausentes"]) >= 1:
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

    if len(raid["discos_ausentes"]) == 0:
        print("Nenhum disco ausente. Reconstrução desnecessária.")
        return

    if len(raid["discos_ausentes"]) > 1:
        print("Erro: mais de um disco ausente. Impossível reconstruir.")
        return

    disco = raid["discos_ausentes"][0]
    tam_bloco = raid["tam_bloco"]
    tam_disco = raid["tam_disco"]
    num_discos = raid["num_discos"]
    pasta = raid["pasta"]
    total_blocos = tam_disco // tam_bloco

    print(f"Reconstruindo disco{disco}.bin...")

    # cria o arquivo novo zerado
    caminho_novo = os.path.join(pasta, f"disco{disco}.bin")
    try:
        with open(caminho_novo, "wb") as f:
            f.write(b"\x00" * tam_disco)
    except Exception as e:
        print(f"Erro ao criar disco{disco}.bin: {e}")
        return

    # reconstrói bloco por bloco
    try:
        for bloco in range(total_blocos):

            pos_bloco = bloco * tam_bloco
            bloco_reconstruido = bytearray(tam_bloco)

            # XOR de todos os outros discos (inclusive paridade)
            for i in range(num_discos):

                if i == disco:
                    continue  

                cam_i = os.path.join(pasta, f"disco{i}.bin")
                with open(cam_i, "rb") as f:
                    f.seek(pos_bloco)
                    bloco_i = f.read(tam_bloco)

                for j in range(len(bloco_i)):
                    bloco_reconstruido[j] ^= bloco_i[j]

            # grava o bloco reconstruído
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
                if raid["num_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    escreve_raid()
            elif opcao == 4:
                if raid["num_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    le_raid()
            elif opcao == 5:
                if raid["num_discos"] == 0:
                    print("Carregue ou inicialize o RAID primeiro!")
                else:
                    remove_disco_raid()
            elif opcao == 6:
                if raid["num_discos"] == 0:
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


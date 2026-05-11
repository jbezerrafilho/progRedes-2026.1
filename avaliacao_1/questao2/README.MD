## Análise de pacotes de rede (20 pontos)

<hr/>

A avaliação de pacotes que trafegam numa rede pode ser útil em muitos casos. A captura do tráfego acontece por meio de programas como *tcpdump*, *pcap* e *winpcap* (ou mesmo em interfaces mais amigáveis, como o *Wireshark*), gerando o que se conhece por formato <b>pcap</b>.
 
O formato do arquivo pcap está disponível em: ```https://datatracker.ietf.org/doc/id/draft-gharris-opsawg-pcap-00.html```

Faça um programa que recebe o nome de um arquivo <b>pcap</b> na linha de comando e **exiba para cada pacote capturado**:

- Os *MAC addresses* de origem e destino do frame;
- Se o protocolo transportado no enlace for IPv4:
  - Mostre os endereços IPv4 de origem e destino;
  - Outros quatro campos do IPv4 à sua escolha;
- Se o protocolo transportado no IPv4 for ICMP:
  - Mostre o nome do tipo do pacote (basta cinco, ignore outros)
  - Para ```echo request``` e ```echo reply```, mostre o número de identificação e o número de sequência.
- Se o protocolo transportado no IPv4 for UDP:
  - Mostre as portas de origem e destino do datagrama;
- Se o protocolo transportado no IPv4 for TCP:
  - Mostre as portas de origem e destino do datagrama;
  - Exiba mais quatro campos a sua escolha;
    
Ao final, mostre:
- o IP da máquina que mais trocou dados usando IPv4 com a máquina de captura, indicando a quantidade de bytes.
- qual o intervalo de tempo em que os pacotes foram capturados.

Não é permitido o uso de bibliotecas não nativas do Python.
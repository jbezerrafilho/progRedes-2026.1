## Servidor de Arquivos em TCP - Especificação  (30 pontos)

<hr/>

A fim de sanar os problemas relatados na questão 1, um servidor de arquivos em TCP deve ser implementado. No entanto, antes disso, um protocolo de comunicação de camada de aplicação deve ser especificado, definindo para cada operação, o que será enviado pelo cliente e o que será respondido pelo servidor. Gere a resposta em formato .pdf (na forma de uma tabela)

Exemplo de uma operação (é só um exemplo da forma de especificação):


| Operação | Cliente Envia | Servidor responde |
|----------|-----------------------|------------------|
|----------|-----------------------|------------------|
| Download | **1 byte** (operação) | **1 byte** (resultado)
| | **4 bytes** (tamanho do nome do arquivo) | **4 bytes** (tamanho do arquivo)
| | **n bytes** (o nome do arquivo) | **n bytes em blocos de 4K** (os dados do arquivo)
| | **Exemplo:**| **resultado:** 0 - significa sucesso
| | B\x00\x00\x00\x08foto.jpg| 1 - arquivo não existe/inacessível
| | | 

|----------|----------|----------|
| Dado D   | Dado E   | Dado F   |   


As operações, sempre iniciadas pelo cliente, a serem especificadas são:

- Listagem dos arquivos disponíveis no servidor;
- Download de um arquivo do servidor;
- Upload de um arquivo ao servidor;
- Solicitação de hash SHA256 de arquivo no servidor (deve enviar a partir de qual byte o hash deve ser calculado);
- Continuação de download de arquivo parcialmente presente no cliente (cliente envia a posição a partir de onde o servidor deve enviar dados do arquivo);
 
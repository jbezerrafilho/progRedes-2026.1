## Cliente e Servidor de arquivos TCP (50 pontos)

<hr/>

Implemente o servidor de arquivos e o respectivo cliente especificados na questão 2. 

Atente para os seguintes pontos:

- Coloque o servidor e o cliente na mesma pasta (nomes: ```questao3_serv.py``` e ```questao3_cli.py```);
- O repositório de arquivos do servidor é na subpasta ```serv_files``` e o do cliente na subpasta ```cli_files```;
- Antes de fazer **download** de arquivos, verifique se o arquivo já existe; Se sim, pergunte ao usuário se deve ou não continuar;
- Jamais grave arquivos fora dos respectivos repositórios do cliente e do servidor (leia sobre o método ```os.path.realpath()```);
- Antes de solicitar a continuação de um **download** parcial, solicite ao servidor o hash do arquivo na parte correspondente à que o cliente já possui. Não solicite a continuação do download se (o hash dos) dados no servidor diferem daqueles do cliente;

Nenhuma biblioteca adicional deve ser instalada no python para que o seu programa funcione.
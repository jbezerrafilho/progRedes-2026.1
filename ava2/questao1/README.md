## Servidor de arquivos usando UDP (20 pontos)

<hr/>

Durante as aulas, foi desenvolvido um servidor de arquivos (programas servidor e cliente) usando o protocolo UDP. Enquanto os programas originais funcionavam para arquivos muito pequenos com apenas um bloco de dados, o mesmo não acontecia para arquivos grandes com muitos blocos sendo enviados/recebidos. Para resolver esse problema, foi colocado um settimeout da API Socket do Python. Explique:

- Por que o timeout isoladamente não é a melhor estratégia para tratar com essa situação.
- Por que mesmo como timeout em uma rede sem maiores problemas de qualidade de sinal (sem perda de pacotes), o UDP não funciona nesse contexto.  

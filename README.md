# RabbitMQ-RPC
Repositório referente a aula realizada em sala, com o objetivo de criar uma comunicação RPC através do RabbitMQ.

## Ferramentas
Para que a atividade possa ter um bom sucesso, foi necessário utilizar as seguintes tecnologias:

- RabbitMQ
- Erlang
- Pika
- Python

Além disso, a IDE utilizada para escrever os códigos foi o Pycharm, por conta da sua ótima integração com o Python.

## Objetivo
O objetivo é criar um sistemas distribuído onde há um servidor principal, responsável por receber as requisições, um cliente que envia essas requisições e também a presença de serviços que são solicitados por ele. 

## Passos
Inicialmente, é preciso executar o arquivo com o servidor principal, para que ele fique aguardando por requisições. Depois disso, em outros terminais, são executados os serviços que podem ser solicitados pelo cliente. E por último o cliente, que faz as requisições de serviços e funciona de maneira remota, seguindo e cumprindo com o objetivo. 

## Exemplo
Um cliente pode solicitar um serviço de soma. Esse serviço é acionado para o servidor, que busca por ele e depois retorna para o cliente uma resposta esperada. Exemplo: entrada de dois valores (a: 5, b: 12). Com esses valores inseridos pelo cliente, o serviço realiza a operação desejada e retorna o resultado, satisfazendo o pedido do cliente. Da mesma forma, os outros serviços também são solicitados e atendidos pelo servidor.

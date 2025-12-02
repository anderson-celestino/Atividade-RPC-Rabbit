#!/usr/bin/env python
import pika
import uuid
import json


class RpcClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, service, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = {
            "service": service,
            "data": data
        }

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_main_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response.decode()


client = RpcClient()

print("Escolha um serviço:")
print("1 - Soma")
print("2 - Multiplicação")
print("3 - Potência")
print("4 - Contador de caracteres")

op = input("Opção: ")

if op == "1":
    a = int(input("a = "))
    b = int(input("b = "))
    print("Resultado:", client.call("soma", {"a": a, "b": b}))

elif op == "2":
    a = int(input("a = "))
    b = int(input("b = "))
    print("Resultado:", client.call("multiplicacao", {"a": a, "b": b}))

elif op == "3":
    base = int(input("Base = "))
    expoente = int(input("Expoente = "))
    print("Resultado:", client.call("potencia", {"base": base, "expoente": expoente}))

elif op == "4":
    texto = input("Texto: ")
    print("Resultado:", client.call("contar", {"texto": texto}))

else:
    print("Opção inválida")

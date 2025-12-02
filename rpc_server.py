#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

# fila em que o CLIENTE envia as requisições
channel.queue_declare(queue='rpc_main_queue')

def on_request(ch, method, props, body):
    request = json.loads(body)

    service = request["service"]
    data = request["data"]

    print(f"[MAIN SERVER] Recebi solicitação para o serviço: {service}")

    # mapeia o serviço -> fila destino
    target_queue = f"rpc_{service}_queue"

    # repassa a requisição para o serviço alvo
    channel.basic_publish(
        exchange='',
        routing_key=target_queue,
        properties=pika.BasicProperties(
            reply_to=props.reply_to,
            correlation_id=props.correlation_id
        ),
        body=json.dumps(data)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

print("[MAIN SERVER] Aguardando requisições...")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_main_queue', on_message_callback=on_request)

channel.start_consuming()

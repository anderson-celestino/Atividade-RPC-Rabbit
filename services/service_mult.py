import json
import pika
from common.rpc_utils import get_connection


def processar(body):
    return {"resultado": body["a"] * body["b"]}


def on_request(ch, method, props, body):
    data = json.loads(body.decode())
    resposta = processar(data)

    print(f"[MULT] Recebido: {data} -> Enviando: {resposta}")

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(resposta)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = get_connection()
channel = connection.channel()

channel.queue_declare(queue="rpc_mult")
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="rpc_mult",
    on_message_callback=on_request,
    auto_ack=False
)

print("[MULTIPLICAÇÃO] Serviço ativo...")
channel.start_consuming()

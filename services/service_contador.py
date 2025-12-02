import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Fila esperada pelo servidor principal
channel.queue_declare(queue='rpc_contar_queue')

def contar(texto):
    return len(texto)

def on_request(ch, method, props, body):
    data = json.loads(body)
    result = contar(data["texto"])

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(result)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

print("[SERVICE CONTAR] aguardando requisições...")
channel.basic_consume(queue='rpc_contar_queue', on_message_callback=on_request)

channel.start_consuming()

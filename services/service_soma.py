import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_soma_queue')

def soma(a, b):
    return a + b

def on_request(ch, method, props, body):
    data = json.loads(body)
    result = soma(data["a"], data["b"])

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(result)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

print("[SERVICE SOMA] aguardando requisições...")
channel.basic_consume(queue='rpc_soma_queue', on_message_callback=on_request)

channel.start_consuming()

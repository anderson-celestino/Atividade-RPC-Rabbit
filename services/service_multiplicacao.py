import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Fila específica do serviço de multiplicação
channel.queue_declare(queue='rpc_multiplicacao_queue')

def multiplicar(a, b):
    return a * b

def on_request(ch, method, props, body):
    data = json.loads(body)

    a = data["a"]
    b = data["b"]

    resultado = multiplicar(a, b)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(resultado)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

print("[SERVICE MULTIPLICACAO] aguardando requisições...")
channel.basic_consume(
    queue='rpc_multiplicacao_queue',
    on_message_callback=on_request
)

channel.start_consuming()

import pika
import uuid
import json


def get_connection():
    """Cria conexão com RabbitMQ."""
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )


class RpcClient:
    def __init__(self):
        self.connection = get_connection()
        self.channel = self.connection.channel()

        # Fila exclusiva para receber respostas do RPC
        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        # Consumidor que ficará ouvindo a fila de retorno
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        """Recebe a resposta do serviço RPC."""
        if props.correlation_id == self.corr_id:
            self.response = json.loads(body.decode())

    def call(self, routing_key, body):
        """Envia requisição RPC e aguarda resposta."""
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(body)
        )

        # Aguarda resposta
        while self.response is None:
            self.connection.process_data_events()

        return self.response

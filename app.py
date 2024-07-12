import ptvsd
from process_events import process_text_event
import pika
import json

ptvsd.enable_attach(address=('0.0.0.0', 5679))

RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'
QUEUE_NAME = 'ai_events'

def callback(ch, method, properties, body):
    event = json.loads(body)
    if event['type'] == 'process_text':
        process_text_event(event['id'])

def consume_events():
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()
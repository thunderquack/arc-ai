import ptvsd

ptvsd.enable_attach(address=('0.0.0.0', 5679))

import redis
import pika
import json
import time

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def process_text_event(task_id):
    redis_client.set(f'task_{task_id}_status', 'in_progress', ex=3600)
    text = redis_client.get(f'task_{task_id}_process_text_ai')
    if text:
        time.sleep(30)  # Симуляция длительной обработки
        processed_text = text.decode('utf-8') + " (processed)"
        redis_client.set(f'task_{task_id}_process_text_ai', processed_text, ex=3600)
        redis_client.set(f'task_{task_id}_status', 'processed', ex=3600)

def callback(ch, method, properties, body):
    event = json.loads(body)
    if event['type'] == 'process_text':
        process_text_event(event['id'])

def consume_events():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='ai_events')

    channel.basic_consume(queue='ai_events', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    consume_events()
import ollama
import redis

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def process_text_event(task_id):
    redis_client.set(f'task_{task_id}_status', 'in_progress', ex=3600)
    text = redis_client.get(f'task_{task_id}_process_text_ai')
    if text:
        text = text.decode('utf-8')
        input = []
        input.append({'role': 'user', 'content': text})
        response = ollama.chat(
            model='mistral-nemo',
            messages=input
        )
        processed_text = response['message']['content']
        redis_client.set(f'task_{task_id}_process_text_ai', processed_text, ex=3600)
        redis_client.set(f'task_{task_id}_status', 'processed', ex=3600)
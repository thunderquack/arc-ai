import ollama
import redis

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def process_text_event(task_id):
    redis_client.set(f'task_{task_id}_status', 'in_progress', ex=3600)
    text = redis_client.get(f'task_{task_id}_process_text_ai')
    if text:
        text = text.decode('utf-8')
        input = []

        prompt = '''After the word "TEXT:", there is a scanned text in German. Correct only the errors and typos without changing the style, structure, or meaning. Return only the corrected text without any explanations or comments. Nothing extra—just the corrected text.
TEXT:
'''
        text = prompt + text
        input.append({'role': 'user', 'content': text})
        try:
            response = ollama.chat(
                model='mistral-nemo',
                messages=input,
                options={"num_ctx": 25600}
            )
            processed_text = response['message']['content']
            redis_client.set(f'task_{task_id}_process_text_ai', processed_text, ex=3600)
            redis_client.set(f'task_{task_id}_status', 'processed', ex=3600)
        except Exception as e:
            redis_client.set(f'task_{task_id}_process_text_ai', e, ex=3600)
            redis_client.set(f'task_{task_id}_status', 'failed', ex=3600)
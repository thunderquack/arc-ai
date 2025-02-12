import redis
#from model import process_text, initialize_model

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Initialize Model (ensure it's only done once)
#model, tokenizer, tokenizer_stream = initialize_model()

def process_text_event(task_id):
    '''
    redis_client.set(f'task_{task_id}_status', 'in_progress', ex=3600)
    text = redis_client.get(f'task_{task_id}_process_text_ai')
    if text:
        text = text.decode('utf-8')
        processed_text = process_text(model, tokenizer, tokenizer_stream, text)
        redis_client.set(f'task_{task_id}_process_text_ai', processed_text, ex=3600)
        redis_client.set(f'task_{task_id}_status', 'processed', ex=3600)
    '''
import onnxruntime_genai as og

MODEL_PATH = '/models/Phi-3/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4'

def initialize_model():
    print("Loading model...")
    model = og.Model(MODEL_PATH)
    tokenizer = og.Tokenizer(model)
    tokenizer_stream = tokenizer.create_stream()
    print("Model loaded")
    return model, tokenizer, tokenizer_stream

def process_text(model, tokenizer, tokenizer_stream, text):
    search_options = {
        'max_length': 1024 * 120,
        'repetition_penalty': 1.2,
    }
    chat_template = '\n{input} \n'
    prompt = f'{chat_template.format(input=text)}'
    input_tokens = tokenizer.encode(prompt)
    
    params = og.GeneratorParams(model)
    params.set_search_options(**search_options)
    params.input_ids = input_tokens
    generator = og.Generator(model, params)
    
    output_text = ""
    while not generator.is_done():
        generator.compute_logits()
        generator.generate_next_token()
        new_token = generator.get_next_tokens()[0]
        output_text += tokenizer_stream.decode(new_token)
    
    del generator
    return output_text
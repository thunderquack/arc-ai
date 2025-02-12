#import onnxruntime_genai as og

def initialize_model():
    return model, tokenizer, tokenizer_stream

def process_text(model, tokenizer, tokenizer_stream, text):
    return output_text
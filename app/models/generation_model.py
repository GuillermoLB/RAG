from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("gpt-neo-125M")

def generate_response(query: str, context: str):
    input_text = f"Context: {context}\nQuery: {query}"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0])

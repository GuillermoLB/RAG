from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the model and tokenizer using the model identifier from the .env file
model_id = os.getenv("GENERATOR_MODEL_ID")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Set the pad_token to eos_token
tokenizer.pad_token = tokenizer.eos_token

def generate_response(query: str, context: str, max_length: int = 512, num_return_sequences: int = 1):
    """
    Generate a response based on the query and context.

    Args:
        query (str): The query string.
        context (str): The context string.
        max_length (int): The maximum length of the generated response.
        num_return_sequences (int): The number of response sequences to generate.

    Returns:
        str: The generated response.
    """
    input_text = f"Context: {context}\nQuery: {query}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
    
    # Decode the generated response
    responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return responses[0] if num_return_sequences == 1 else responses

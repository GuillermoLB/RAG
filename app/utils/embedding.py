from loguru import logger
from transformers import AutoTokenizer, AutoModel
import torch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the model and tokenizer using the model identifier from the .env file
model_id = os.getenv("EMBED_MODEL_ID")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)

def get_embeddings(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def embed_chunks(chunks):
    logger.info("Embedding chunks")
    chunk_data = []
    for i, chunk in enumerate(chunks):
        txt_tokens = len(tokenizer.tokenize(chunk.text, max_length=None))
        embedding = get_embeddings(chunk.text)
        chunk_info = {
            "index": i,
            "chunk_text": chunk.text,
            "chunk_text_tokens": txt_tokens,
            "embedding": embedding,
        }
        chunk_data.append(chunk_info)
    logger.info(f"Chunked {len(chunks)} chunks")
    return chunk_data
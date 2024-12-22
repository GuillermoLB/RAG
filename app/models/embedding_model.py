from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(text: str):
    return model.encode(text, convert_to_tensor=True)

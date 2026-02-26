from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
import numpy as np

# Load the embedding model once
model = SentenceTransformer(EMBEDDING_MODEL)


def embed_text(text):
    # Convert text into a vector embedding for semantic search.
    # Returns a list of 384 floats (since all-MiniLM-L6-v2 produces 384-dim vectors).
    if not text or not isinstance(text, str):
        return [0.0] * 384
    
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()


def embedding_to_pgvector_string(embedding):
    # Convert embedding list to PostgreSQL pgvector format string.
    return "[" + ",".join(str(x) for x in embedding) + "]"

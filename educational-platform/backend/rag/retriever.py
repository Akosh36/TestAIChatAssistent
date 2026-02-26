from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Article
from rag.embeddings import embed_text
from config import RAG_TOP_K


def search_similar_articles(db: Session, query: str, section: str = None, language: str = "en", top_k: int = RAG_TOP_K):
    # Find articles most similar to the user query using vector similarity (cosine distance).
    # Optionally filter by section and language.
    # Returns list of Article objects with highest similarity to the query.
    
    # Embed the user query
    query_embedding = embed_text(query)
    
    # Build base query filtered by language
    base_query = db.query(Article).filter(Article.language == language)
    
    # Optional: filter by section
    if section:
        base_query = base_query.filter(Article.section == section)
    
    # Order by vector distance (cosine distance using <-> operator) and limit to top_k
    # PostgreSQL pgvector extension provides the <-> operator for cosine distance
    articles = base_query.order_by(
        func.l2(Article.embedding, query_embedding)
    ).limit(top_k).all()
    
    return articles

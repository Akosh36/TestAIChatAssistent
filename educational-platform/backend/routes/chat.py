import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import ChatMessage, User
from rag.retriever import search_similar_articles
from rag.embeddings import embed_text
from config import OLLAMA_URL, OLLAMA_MODEL
from routes.auth import verify_jwt_token

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    section: str = None  # Optional: which subject section this is about
    language: str = "en"  # en, uz, or ru
    token: str = None  # Optional: JWT token for authenticated users


def build_prompt(question: str, articles: list, language: str) -> str:
    # Build a prompt for Ollama with retrieved context articles and user question.
    # Returns formatted prompt that guides the AI to answer in the specified language.
    
    context = "\n\n".join([f"Title: {a.title}\n{a.body}" for a in articles])
    
    return f"""You are a helpful educational assistant.
Use the following educational content to answer the user's question accurately.
Always respond in {language}.
If the content doesn't contain the answer, say "I don't have enough information about this topic."

EDUCATIONAL CONTENT:
{context}

QUESTION: {question}

ANSWER:"""


def ask_ollama(prompt: str) -> str:
    # Send prompt to Ollama and get AI response.
    # Returns plain text response from the llama3 model.
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")
        
        data = response.json()
        return data.get("response", "").strip()
    
    except requests.exceptions.ConnectionError:
        return "Sorry, I cannot connect to the AI service right now. Please try again later."
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Send user message and get AI response using RAG pipeline.
    # Retrieves relevant articles, builds prompt, calls Ollama, and returns response.
    # Optionally saves chat history for authenticated users.
    
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail={"error": "Message cannot be empty"})
    
    # Step 1: Retrieve relevant articles using RAG
    articles = search_similar_articles(
        db,
        query=request.message,
        section=request.section,
        language=request.language,
        top_k=3
    )
    
    if not articles:
        # If no articles found, still ask Ollama but without context
        articles = []
    
    # Step 2: Build prompt with context
    prompt = build_prompt(request.message, articles, request.language)
    
    # Step 3: Get response from Ollama
    reply = ask_ollama(prompt)
    
    # Step 4: Save chat history if user is authenticated
    if request.token:
        try:
            email = verify_jwt_token(request.token)
            user = db.query(User).filter(User.email == email).first()
            if user:
                chat_message = ChatMessage(
                    user_id=user.id,
                    message=request.message,
                    reply=reply,
                    section=request.section or "general",
                    language=request.language
                )
                db.add(chat_message)
                db.commit()
        except:
            # If token verification fails, don't save history but still return response
            pass
    
    return {"reply": reply}

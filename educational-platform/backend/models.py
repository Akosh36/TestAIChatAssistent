from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import VECTOR
from datetime import datetime
from database import Base


class User(Base):
    # Store user account information.
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Article(Base):
    # Store educational content articles with embeddings for RAG search.
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    section = Column(String, index=True)  # math, programming, science, history, languages, general
    title = Column(String)
    body = Column(Text)
    language = Column(String, index=True)  # en, uz, ru
    embedding = Column(VECTOR(384), nullable=True)  # Vector from all-MiniLM-L6-v2 model
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    # Store chat history for logged-in users (RAG pipeline logs).
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)  # User question
    reply = Column(Text)  # AI response
    section = Column(String)  # Which subject section the chat was about
    language = Column(String)  # en, uz, ru
    created_at = Column(DateTime, default=datetime.utcnow)


class Bookmark(Base):
    # Store user bookmarks for quick access to saved articles.
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

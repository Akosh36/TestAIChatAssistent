from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Article, Bookmark, User
from routes.auth import verify_jwt_token

router = APIRouter(prefix="/api/content", tags=["content"])

# All sections available in the platform
SECTIONS = ["math", "programming", "science", "history", "languages", "general"]
SECTION_LABELS = {
    "en": {
        "math": "Mathematics",
        "programming": "Programming",
        "science": "Science",
        "history": "History",
        "languages": "Languages",
        "general": "General"
    },
    "uz": {
        "math": "Matematika",
        "programming": "Dasturlash",
        "science": "Fanlar",
        "history": "Tarix",
        "languages": "Tillar",
        "general": "Umumiy"
    },
    "ru": {
        "math": "Математика",
        "programming": "Программирование",
        "science": "Наука",
        "history": "История",
        "languages": "Языки",
        "general": "Общее"
    }
}


class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    section: str
    language: str


class SectionResponse(BaseModel):
    id: int
    name: str
    label: str


@router.get("/sections")
def get_sections(language: str = "en"):
    # Get all available study sections with labels in the requested language.
    # Returns list of sections with id, name (system name), and label (translated name).
    
    if language not in SECTION_LABELS:
        language = "en"
    
    sections = [
        {
            "id": idx,
            "name": section,
            "label": SECTION_LABELS[language].get(section, section)
        }
        for idx, section in enumerate(SECTIONS, 1)
    ]
    
    return sections


@router.get("/{section}")
def get_section_articles(section: str, language: str = "en", db: Session = Depends(get_db)):
    # Get all articles in a specific section and language.
    # Returns list of articles with title and body content.
    
    if section not in SECTIONS:
        raise HTTPException(status_code=404, detail={"error": "Section not found"})
    
    articles = db.query(Article).filter(
        Article.section == section,
        Article.language == language
    ).all()
    
    if not articles:
        raise HTTPException(status_code=404, detail={"error": "No articles found for this section and language"})
    
    return [
        {
            "id": article.id,
            "title": article.title,
            "body": article.body,
            "section": article.section,
            "language": article.language
        }
        for article in articles
    ]


@router.get("/search")
def search_articles(q: str, lang: str = "en", db: Session = Depends(get_db)):
    # Search articles by title or body content.
    # Uses full-text search to find relevant articles in the specified language.
    
    if not q:
        raise HTTPException(status_code=400, detail={"error": "Search query cannot be empty"})
    
    search_term = f"%{q}%"
    articles = db.query(Article).filter(
        Article.language == lang,
        (Article.title.ilike(search_term) | Article.body.ilike(search_term))
    ).limit(10).all()
    
    return [
        {
            "id": article.id,
            "title": article.title,
            "body": article.body,
            "section": article.section,
            "language": article.language
        }
        for article in articles
    ]


@router.post("/bookmarks")
def add_bookmark(article_id: int, token: str, db: Session = Depends(get_db)):
    # Add an article to user's bookmarks. Requires JWT authentication.
    # Returns success message or error if article not found or already bookmarked.
    
    email = verify_jwt_token(token)
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail={"error": "User not found"})
    
    # Check if article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail={"error": "Article not found"})
    
    # Check if bookmark already exists
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == user.id,
        Bookmark.article_id == article_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail={"error": "Article already bookmarked"})
    
    # Add bookmark
    bookmark = Bookmark(user_id=user.id, article_id=article_id)
    db.add(bookmark)
    db.commit()
    
    return {"message": "Article bookmarked"}


@router.get("/bookmarks")
def get_bookmarks(token: str, db: Session = Depends(get_db)):
    # Get all bookmarked articles for authenticated user.
    # Returns list of bookmarked articles with titles and details.
    
    email = verify_jwt_token(token)
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail={"error": "User not found"})
    
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user.id).all()
    
    results = []
    for bookmark in bookmarks:
        article = db.query(Article).filter(Article.id == bookmark.article_id).first()
        if article:
            results.append({
                "article_id": article.id,
                "title": article.title,
                "section": article.section,
                "language": article.language
            })
    
    return results

# 🎓 Educational AI Learning Platform

A multilingual educational platform with an AI chat assistant, built with FastAPI backend, PostgreSQL database, and Ollama AI integration.

## 🎯 Features

- **Multilingual Support**: English, Uzbek, and Russian
- **AI Chat Assistant**: RAG-based AI that retrieves relevant educational content before answering
- **6 Subject Sections**: Mathematics, Programming, Science, History, Languages, General
- **User Authentication**: JWT-based login and registration
- **Bookmarks**: Save favorite articles for quick access
- **Chat History**: For authenticated users
- **Responsive Design**: Works on desktop and mobile

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
      ↓↑ REST API (JSON)
Backend (FastAPI)
      ↓↑
PostgreSQL + pgvector
      ↓↑
Ollama AI (llama3)
```

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development without Docker)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
cd educational-platform
docker-compose up
```

Wait for services to start (check "healthy" status):
```bash
docker-compose ps
```

Then seed the database:
```bash
docker-compose exec backend python seed.py
```

Open browser: `http://localhost:8000`

### Option 2: Local Development

#### 1. Start PostgreSQL

```bash
docker pull pgvector/pgvector:pg15
docker run -d \
    -e POSTGRES_DB=eduplatform \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=password \
    -p 5432:5432 \
    pgvector/pgvector:pg15
```

#### 2. Start Ollama

```bash
docker pull ollama/ollama
docker run -d \
    -p 11434:11434 \
    -v ollama_data:/root/.ollama \
    ollama/ollama

# Pull the llama3 model
docker exec -it <container_id> ollama pull llama3
```

#### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 4. Seed the Database

```bash
cd backend
python seed.py
```

#### 5. Start Backend

```bash
cd backend
python main.py
```

Backend runs on `http://localhost:8000`

#### 6. Serve Frontend

```bash
# Option A: Simple HTTP server
cd frontend
python -m http.server 8080

# Option B: Use a web server like nginx
```

Frontend will be on `http://localhost:8080` (or your configured port)

## 📡 API Endpoints

### Authentication

```
POST /api/auth/register
  { "email": "user@example.com", "password": "secret" }
  → { "message": "User registered successfully" }

POST /api/auth/login
  { "email": "user@example.com", "password": "secret" }
  → { "token": "jwt_token_here" }
```

### Content

```
GET /api/content/sections?language=en
  → [{ "id": 1, "name": "math", "label": "Mathematics" }]

GET /api/content/{section}?language=en
  → [{ "id": 1, "title": "Algebra Basics", "body": "...", "section": "math" }]

GET /api/content/search?q=algebra&lang=en
  → [{ "id": 1, "title": "Algebra Basics", "body": "..." }]

POST /api/content/bookmarks
  { "article_id": 5, "token": "jwt_token" }
  → { "message": "Article bookmarked" }

GET /api/content/bookmarks?token=jwt_token
  → [{ "article_id": 5, "title": "Algebra Basics", "section": "math" }]
```

### Chat (RAG Pipeline)

```
POST /api/chat
  {
    "message": "What is the Pythagorean theorem?",
    "section": "math",
    "language": "en",
    "token": "jwt_token" (optional)
  }
  → { "reply": "The Pythagorean theorem states..." }
```

## 📚 Database Schema

### Users
```sql
- id (primary key)
- email (unique)
- password_hash
- created_at
```

### Articles (with pgvector embeddings)
```sql
- id (primary key)
- section (math, programming, science, history, languages, general)
- title
- body
- language (en, uz, ru)
- embedding (vector 384-dim)
- created_at
```

### Chat Messages
```sql
- id (primary key)
- user_id (foreign key)
- message
- reply
- section
- language
- created_at
```

### Bookmarks
```sql
- id (primary key)
- user_id (foreign key)
- article_id (foreign key)
- created_at
```

## 🤖 RAG Pipeline Explained

1. **User Question** → Embedded using sentence-transformers
2. **Vector Search** → Find top 3 most similar articles in PostgreSQL using pgvector
3. **Context Building** → Combine relevant article bodies as context
4. **Prompt Creation** → Format question + context into a prompt
5. **Ollama Call** → Send prompt to llama3 model via REST API
6. **Response** → Return AI-generated answer to user

**Key File**: `backend/routes/chat.py` contains the full pipeline

## 📝 Seed Data

The platform comes with 54 educational articles:
- 6 sections × 3 languages × 3 articles = 54 articles total
- Each article includes:
  - Title
  - Detailed educational content
  - Vector embedding (generated automatically)

Run `python seed.py` to populate the database.

## 🎨 Frontend Structure

```
/frontend
├── index.html          # Single page application
├── css/
│   └── style.css       # All styles (responsive design)
└── js/
    ├── main.js         # Navigation, language switching, auth
    └── chat.js         # Chat widget logic
```

### Key Features:

- **Language Switching**: Change EN/UZ/RU instantly
- **Section Navigation**: Click cards to browse articles
- **Chat Widget**: Floating button opens chat drawer
- **Local Storage**: Remembers language preference and chat history
- **Responsive Design**: Mobile-friendly layout

## 🔐 Authentication Flow

1. **Register**: Create account with email + password
2. **Login**: Get JWT token
3. **Store Token**: Save in localStorage
4. **API Calls**: Send `token` in request body to protected endpoints
5. **Chat History**: Only saved for logged-in users

## 🧪 Testing

### Test Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is algebra?",
    "section": "math",
    "language": "en",
    "token": null
  }'
```

## 📦 Configuration

Edit `backend/config.py` to change:
- Database URL
- Ollama URL and model
- JWT secret (change for production!)
- Embedding model
- RAG retrieval parameters

## 🐳 Docker Compose Reference

### View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f ollama
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Images

```bash
docker-compose build --no-cache
```

## 📋 Code Rules

Every file follows these principles:
1. **One file = one responsibility**
2. **No clever code** - readable by junior devs in 30 seconds
3. **Comment every function** - one-line explanation
4. **Descriptive variable names** - `user_question`, not `q`
5. **Clean JSON APIs** - no nested wrappers
6. **Readable error messages** - `{"error": "User not found"}`

## 🚨 Common Issues

### Ollama Connection Error

```
Error: Cannot connect to http://localhost:11434
```

**Solution**: Make sure Ollama container is running and model is pulled
```bash
docker exec <ollama_container> ollama pull llama3
```

### pgvector Extension Not Found

```
Error: type "vector" does not exist
```

**Solution**: Use `pgvector/pgvector` image in docker-compose (already configured)

### CORS Errors in Frontend

**Solution**: CORS is enabled for all origins (`*`) in `backend/main.py`

### Chat Returns Empty Response

**Solution**: 
1. Check Ollama is running: `curl http://localhost:11434/api/tags`
2. Check database is seeded: `python seed.py`
3. Check database connection in logs

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `config.py` | All configuration in one place |
| `database.py` | SQLAlchemy setup and session management |
| `models.py` | Database table definitions |
| `seed.py` | Populate database with 54 articles |
| `routes/auth.py` | JWT login/register endpoints |
| `routes/content.py` | Article browsing & bookmarks |
| `routes/chat.py` | RAG pipeline & AI chat |
| `rag/embeddings.py` | Text embedding (sentence-transformers) |
| `rag/retriever.py` | Vector similarity search (pgvector) |
| `main.py` | FastAPI app initialization |

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **pgvector**: https://github.com/pgvector/pgvector
- **Ollama**: https://ollama.ai/
- **Sentence Transformers**: https://www.sbert.net/

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow the code rules (comments, clear names, readable code).

## 📞 Support

For issues or questions:
1. Check the "Common Issues" section above
2. Review the API documentation at `http://localhost:8000/docs`
3. Check logs: `docker-compose logs -f`

---

**Built with ❤️ for education**

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes import auth, content, chat
from config import SERVER_HOST, SERVER_PORT, DEBUG

# Create FastAPI app
app = FastAPI(
    title="Educational AI Platform",
    description="A multilingual educational platform with AI chat assistant",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(chat.router)


@app.get("/health")
def health_check():
    # Health check endpoint for monitoring.
    return {"status": "ok"}


@app.get("/")
def root():
    # API welcome message and documentation link.
    return {
        "message": "Educational AI Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=DEBUG
    )

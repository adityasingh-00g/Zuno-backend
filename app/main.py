from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.chat import router as chatRouter
from app.api.v1.documentUpload import router as docUploadRouter
from app.rag.embeddings import warmup_embeddings

# Create FastAPI app
app = FastAPI(title="RAG BACKEND")

# Startup event (ADD THIS)
@app.on_event("startup")
def startup_event():
    warmup_embeddings()
    
# Enable CORS so your React frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chatRouter, prefix="/api/v1")
app.include_router(docUploadRouter,prefix="/api/v1")

# Optional: Root endpoint for testing
@app.get("/")
def root():
    return {"message": "RAG Backend is running!"}



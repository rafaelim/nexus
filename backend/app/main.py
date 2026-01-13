from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import transactions, categories, expenses, notes

app = FastAPI(
    title="Nexus API",
    description="Multi-domain home management API for tracking finances, household expenses, groceries, and more",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(expenses.router, prefix="/api/v1/expenses", tags=["expenses"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])


@app.get("/")
def root():
    return {"message": "Nexus API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


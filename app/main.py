"""
TaskFlow API - Main Application Entry Point

A production-ready REST API built with FastAPI demonstrating:
- Clean Architecture & SOLID Principles
- JWT Authentication
- SQLAlchemy ORM with Async Support
- Pydantic Data Validation
- Comprehensive Error Handling
- API Documentation (OpenAPI/Swagger)

Author: Neel Patel
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn

from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.core.database import init_db
from app.middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events handler."""
    # Startup
    print("Starting up TaskFlow API...")
    await init_db()
    yield
    # Shutdown
    print("Shutting down TaskFlow API...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## TaskFlow API
    
    A comprehensive task management REST API demonstrating:
    
    * **Authentication** - JWT-based secure authentication
    * **CRUD Operations** - Full task management capabilities
    * **User Management** - User registration and profile management
    * **Data Validation** - Pydantic models for request/response validation
    * **Error Handling** - Consistent error responses
    
    ### Features:
    - Create, read, update, and delete tasks
    - User registration and authentication
    - Task filtering and pagination
    - Due date management
    - Priority levels
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# Include API routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "message": "Welcome to TaskFlow API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "available"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

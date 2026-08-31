"""
AI Marketing Content Engine — FastAPI Application

Main application entry point with CORS, health check, exception handlers, and API router mounting.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.llm import LLMProviderError, LLMValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    print(f"🚀 {settings.app_name} starting...")
    print(f"   Environment: {settings.app_env}")
    print(f"   Debug: {settings.debug}")
    print(f"   LLM Provider: {settings.llm_provider}")
    yield
    print(f"👋 {settings.app_name} shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered marketing content generation across LinkedIn, X/Twitter, Instagram, and Blog.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS Middleware ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Exception Handlers ─────────────────────────────────────
@app.exception_handler(LLMProviderError)
async def llm_provider_exception_handler(request: Request, exc: LLMProviderError):
    """Handle LLM provider API failures gracefully."""
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": f"LLM Provider Error: {str(exc)}"},
    )


@app.exception_handler(LLMValidationError)
async def llm_validation_exception_handler(request: Request, exc: LLMValidationError):
    """Handle output schema validation failures after retries."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": f"LLM Output Schema Validation Failed: {str(exc)}"},
    )


# ── API Routers ──────────────────────────────────────────────────
from app.api.v1 import api_v1_router

app.include_router(api_v1_router)


# ── Health Check ─────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ── Root ─────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info."""
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

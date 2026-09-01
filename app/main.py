"""Main FastAPI application."""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html

from app.api.routes import auth, authors, books, health, publishers
from app.config import settings
from app.database.mongodb import MongoDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("Starting Book Library API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"MongoDB URI: {settings.MONGO_URI}")

    try:
        await MongoDB.connect()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Book Library API")
    await MongoDB.disconnect()
    logger.info("Application shutdown complete")


# Create FastAPI application with explicit docs configuration
app = FastAPI(
    title="Book Library API",
    description="RESTful API for managing books and authors with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url=None,  # We'll use a custom ReDoc endpoint
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(publishers.router)


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Root endpoint - API information."""
    return {
        "message": "Welcome to Book Library API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }


def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Book Library API",
        version="1.0.0",
        description="Production-ready REST API for managing books and authors with JWT authentication",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Serve ReDoc documentation."""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Book Library API - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.is_development(),
    )

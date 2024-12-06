from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # For serving static files
from app.api.v1.endpoints import router as api_router
from app.db.base import Base, engine

# Create the FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(api_router, prefix="/api/v1")

# Root endpoint to serve the main HTML file
@app.get("/")
def serve_home():
    return {"message": "Frontend is accessible via /static/index.html"}

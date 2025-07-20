from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import auth, user, feedback, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Internal Feedback Tool API",
    description="A tool for structured feedback sharing between managers and team members",
    version="1.0.0"
)

# List of allowed origins (add your frontend URL here)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
]

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["Content-Disposition"],  # Expose additional headers if needed
)

# Add middleware to handle CORS preflight requests
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    if request.method == "OPTIONS":
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.status_code = 200
    return response

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(feedback.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Internal Feedback Tool API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import endpoints as v1_endpoints

app = FastAPI(title="Maze Adventure Game API")

app.include_router(v1_endpoints.router, prefix="/api/v1", tags=["v1"])

# Configure CORS middleware
origins = [
    "http://localhost:5173", # Allow requests from the Vue development server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Maze Adventure Game API!"}

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.endpoints import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

def backend_entrypoint() -> None:
    """
    Run backend application
    """
    logging.basicConfig(level=logging.INFO)

    uvicorn.run("backend.__main__:app", host="0.0.0.0", port=8000, workers=2)

if __name__ == "__main__":
    backend_entrypoint()

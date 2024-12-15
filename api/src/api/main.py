import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .clients.postgres import PostgresVectorClient
from .routes import router
from .utils import log

log.init(os.getenv("LOG_LEVEL", "INFO"))

logger = log.get_logger(__name__)

api_reload = os.getenv("API_RELOAD", "False").lower() == "true"

app = FastAPI(title="Cillers Footway Hackathon Demo API", version="1.0.0")
app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    vector_client = PostgresVectorClient()
    vector_client.initialize_table()
    await vector_client.load_sample_data()

def main():
    api_port = os.getenv("API_PORT")
    if not api_port:
        raise ValueError("API_PORT environment variable is not set")

    logger.info(f"Starting API on port {api_port}")
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=int(api_port),
        reload=api_reload,
    )

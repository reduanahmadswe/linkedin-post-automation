from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.config import load_env
from app.database import init_db
from routes.approval_routes import router as approval_router
from utils.logger import setup_logger

app = FastAPI()

setup_logger()
load_env()
init_db()
start_scheduler()

app.include_router(approval_router)

@app.get("/")
def root():
    return {"message": "LinkedIn AI Poster is running!"}

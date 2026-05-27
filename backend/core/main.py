from fastapi import FastAPI
from core.api import router
from core.db import engine, Base

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Construction Planner ML")

app.include_router(router)
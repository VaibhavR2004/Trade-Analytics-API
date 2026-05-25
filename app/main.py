from fastapi import FastAPI
from app.database import engine, Base
from app import models

from app.routers import (
    analytics,
    predictions,
    auth_routers
)

import app.models


try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("Running in development mode without database")

app = FastAPI(
    title="Trade Analytics API",
    version="1.0.0"
)

app.include_router(
    auth_routers.router
)

app.include_router(
    analytics.router
)

app.include_router(
    predictions.router
)
@app.get("/")
def home():
    return {
        "message": "Trade Analytics Backend Running"
    } 
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.database.database import db_client
from app.middleware.auth import FingerprintMiddleware

load_dotenv()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="TgMiniAppsTemplate Backend",
    openapi_url="/api/v1/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
scheduler = AsyncIOScheduler()
# Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(FingerprintMiddleware)
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await db_client.create_db()
    await db_client.clear_db()
    scheduler.add_job(db_client.clear_db, IntervalTrigger(hours=1))
    scheduler.start()

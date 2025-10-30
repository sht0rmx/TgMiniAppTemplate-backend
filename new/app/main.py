from app.middleware.auth import FingerprintMiddleware
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database.database import db_client
from app.api.main import api_router


load_dotenv()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="TgMiniAppsTemplate Backend",
    openapi_url=f"/api/v1/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(FingerprintMiddleware)
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await db_client.create_db()
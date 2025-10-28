from fastapi import APIRouter


router = APIRouter(prefix="/ping", tags=["ping"])
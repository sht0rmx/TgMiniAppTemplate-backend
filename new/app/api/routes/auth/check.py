from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(tags=["check"])

@router.get("/", dependencies=[])
def check():
    user = ...
    JSONResponse({"user":user}, status_code=200)


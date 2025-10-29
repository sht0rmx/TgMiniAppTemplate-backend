from fastapi import APIRouter


router = APIRouter(prefix="/botupdates", tags=["bot-ws"])


@router.websocket("/")
def bot_updates():
    ...
from datetime import datetime
import os
import hmac
import uuid
import hashlib

from app.database.models.Users import User
from app.utils import is_date_expired
from dotenv import load_dotenv
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession

from app.database.models import Base
from app.database.models.RefreshSessions import RefreshSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(str(DATABASE_URL), echo=True)


class DBError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class NotFound(DBError):
    pass

class Revoked(DBError):
    pass

class Expired(DBError):
    pass

class Database:
    def __init__(self):
        self.engine = engine
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        
    async def get_refresh_session(self, refresh_token:str, fingerprint:str) -> RefreshSession:
        async with self.async_session() as dbsession:
            result = await dbsession.execute(select(RefreshSession).where(
                RefreshSession.refresh_token_hash == refresh_token,
                RefreshSession.fingerprint == fingerprint
            ))
            session = result.scalars().first()
            
            if not session:
                raise NotFound("Session with tis params not founded!")
            
            if session.revoked is True:
                raise Revoked("Session was revoked!")
            
            if is_date_expired(created=session.created_at, expire_delta=str(os.getenv("REFRESH_EXPIRE"))):
                raise Expired("Session expired!")
            
            return session
    
    async def update_refresh_session(self, refresh_token:str, fingerprint:str, user_id:uuid.UUID):
        async with self.async_session() as dbsession:
            
            await dbsession.execute(delete(RefreshSession).where(
                RefreshSession.fingerprint == fingerprint
            ))
            
            token_hash = hmac.new(key=str(os.getenv("REFRESH_SECRET")).encode("utf-8"),
                                msg=refresh_token.encode("utf-8"),
                                digestmod=hashlib.sha256)
            
            await dbsession.execute(
                insert(RefreshSession).values(
                    user_id=user_id,
                    refresh_token_hash=token_hash,
                    fingerprint=fingerprint,
                    created_at=datetime.now()
                )
            )
            
            return True
        
    async def update_user(self, telegram_id:int, username:str, name:str, avatar_url:str, role="user"):
        async with self.async_session() as dbsession:
            result = await dbsession.execute(select(User).where(
                User.telegram_id == telegram_id
            ))
            
            user = result.scalars().first()
            
            if not user:
                await dbsession.execute(
                    insert(User).values(
                        telegram_id=telegram_id,
                        username=username,
                        name=name,
                        avatar_url=avatar_url,
                        last_seen=datetime.now(),
                        created_at=datetime.now()
                    )
                )
                
                return True
    
    async def get_user(self, uuid:str="", telegram_id:int=0, username:str=""):
        async with self.async_session() as dbsession:
            ...
        
    
    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()

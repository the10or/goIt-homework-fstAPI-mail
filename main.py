import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from api.contacts_router import router as contacts_router
from api.auth import router as auth_router
from dependencies.database import engine
from models import contacts
from config import REDIS_HOST, REDIS_PORT

contacts.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

origins = ["127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/api", tags=["auth"])


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def health_check():
    return {"status": "ok"}

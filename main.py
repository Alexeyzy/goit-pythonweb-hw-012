from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.database.db import Base, engine
from src.routes.auth import router as auth_router
from src.routes.contacts import router as contacts_router
from src.routes.users import limiter, router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Final Contacts API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(contacts_router, prefix="/api")


@app.get("/")
def root() -> dict[str, str]:
    """Return application health message."""
    return {"message": "Final Contacts API is running"}

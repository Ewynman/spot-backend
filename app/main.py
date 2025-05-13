from fastapi import FastAPI
from .routes import spots
from .routes import users
from .routes import follow 
from .routes import friends
from .db import Base, engine

app = FastAPI()

# ✅ Create tables on startup
Base.metadata.create_all(bind=engine)

# ✅ Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ✅ Register all routers
app.include_router(users.router)
app.include_router(spots.router)
app.include_router(follow.router)
app.include_router(friends.router)

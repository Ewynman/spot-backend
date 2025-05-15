from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import spots, users, follow, friends
from .db import Base, engine

app = FastAPI()

# ✅ CORS middleware to allow mobile frontend to make API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://your-phone-ip:port"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

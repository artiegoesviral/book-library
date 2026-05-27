from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from db import Base, engine

from routers.auth_router import router as auth_router
from routers.library import router as library_router

from models.user_model import User
from models.library_item_model import LibraryItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(library_router)


@app.get("/")
def root():
    return {"message": "API running"}
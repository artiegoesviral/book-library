from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from db import engine, SessionLocal, Base
from models import user_model 
from models.user_model import User
from models.library_item_model import LibraryItem
from auth import get_password_hash 
from routers.library_router import router as library_router 
from routers.auth_router import router as auth_router
from routers.user_router import router as user_router

app = FastAPI(title="Book Database") 

origins = [ "http://localhost:4200", "http://127.0.0.1:8000" ] 

app.add_middleware( CORSMiddleware, 
allow_origins=[
    "http://localhost:4200",
    "http://127.0.0.1:4200"
], 
allow_credentials=True,
allow_methods=["*"], 
allow_headers=["*"], ) 

app.include_router(library_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/") 
def read_root(): 
    return {"message": "Server working correctly"}

Base.metadata.create_all(bind=engine)
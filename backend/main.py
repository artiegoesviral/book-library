from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, SessionLocal
from models import user_model
from models.user_model import User
# from src.routers.user_router import router as user_router
# from src.routers.auth_router import router as auth_router
# from src.routers.table_router import router as table_router
# from src.routers.reservation_router import router as reservation_router
# from src.routers.review_router import router as review_router
# from src.routers.menu_router import router as menu_router
from auth import get_password_hash

# Inicializar FastAPI
app = FastAPI(title="CRM Restaurante")

# Configurar CORS
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Servidor funcionando correctamente"}

user_model.Base.metadata.create_all(bind=engine)
# table_model.Base.metadata.create_all(bind=engine)
# reservation_model.Base.metadata.create_all(bind=engine)
# review_model.Base.metadata.create_all(bind=engine)
# menu_model.Base.metadata.create_all(bind=engine)

# app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(auth_router, prefix="/users/auth", tags=["Auth"])
# app.include_router(table_router)
# app.include_router(reservation_router)
# app.include_router(review_router)
# app.include_router(menu_router)

def create_default_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.name == "admin").first()
    
    if not admin:
        new_admin = User(
            name="admin",
            email="admin@restaurant.com",
            password=get_password_hash("admin123"),
            is_admin=False
        )
        db.add(new_admin)
        db.commit()
    
    db.close()

create_default_admin()
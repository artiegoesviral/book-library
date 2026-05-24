from pydantic import BaseModel                    # Validación de datos

class UserCreate(BaseModel):                      # Datos que recinimos al crear
    name: str
    email: str
    password: str

class UserRead(UserCreate):                       # Datos que devolvemos
    id: int

    class Config:
        from_attributes = True                    # Permite coonvertir desde OMR(Object Relational Mapping)

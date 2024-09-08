from pydantic import BaseModel, EmailStr

class Cliente(BaseModel): 
    cedula : str
    nombre : str
    apellido : str
    correo : EmailStr
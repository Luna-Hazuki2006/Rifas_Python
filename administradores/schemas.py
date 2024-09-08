from pydantic import BaseModel, EmailStr

class Administrador(BaseModel): 
    cedula : str
    nombre : str
    apellido : str
    correo : EmailStr
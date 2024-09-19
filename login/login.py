from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi import Security
from datetime import datetime, timezone, timedelta
from bd import Jugadores, Administradores
from pydantic import BaseModel, EmailStr

class Usuario(BaseModel): 
    cedula : str
    nombre : str
    apellido : str
    correo : EmailStr
    contraseña : str

class Creacion(Usuario): 
    tipo : str

class Inicio(BaseModel): 
    cedula : str
    contraseña : str

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "27A0D7C4CCCE76E6BE39225B7EEE8BD0EF890DE82D49E459F4C405C583080AB0"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Hubo un error en el iniciar sesión')
        except jwt.JWTError as e:
            raise Exception('Se expiró la sesión')
        # except Exception as e:
        #     raise RequiresLoginException()
        #!comentado esto de arriba para no morir en el intento de debbugear
            
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes= self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        #to_encode = {"exp": expire, "sub": str(subject)} Si no funciona lo de arriba toca esto
        
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)


    def verify_password(self, plain_password, hash_password):
        return self.pwd_context.verify(plain_password, hash_password)


    async def authenticate_user(self, cedula: str, contraseña: str, tipo : str):
        try:
            usuario = obtener_usuario(cedula, tipo)
            if usuario: 
                # password_check = self.verify_password(contraseña, usuario.contraseña)
                # if password_check: 
                if contraseña == usuario.contraseña: 
                    return usuario
                else: 
                    return False
                #return password_check #Nuestro código original retornaba el usuario (?)
                #por una buena razon lo retornaba
            else: 
                return False
        except:
            raise Exception('Se necesita iniciar sesión')

# MODIFICAR
def obtener_usuario(cedula : str, tipo : str): 
    if tipo == 'cliente': 
        usuario = Jugadores.find_one({'cedula': cedula})
    elif tipo == 'admin' or tipo == 'administrador': 
        usuario = Administradores.find_one({'cedula': cedula})
    usuario = Usuario(
        cedula=usuario['cedula'], 
        nombre=usuario['nombre'], 
        apellido=usuario['apellido'], 
        correo=usuario['correo'], 
        contraseña=usuario['contraseña']
    )
    return usuario
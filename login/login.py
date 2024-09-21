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

class Message_Redirection_Exception(Exception):
    def __init__ (self, message: str, path_route: str, path_message: str):
        self.message = message
        self.path_route = path_route
        self.path_message = path_message

class No_Administrador_Exception(Message_Redirection_Exception):
    def __init__(self, message='Para acceder a esta función debes ser otro tipo de usuario.', path_route='/', path_message='Volver a home.'):
        super().__init__(message, path_route, path_message)

class No_Cliente_Exception(Message_Redirection_Exception):
    def __init__(self, message='Para acceder a esta función debes ser otro tipo de usuario.', path_route='/', path_message='Volver a home.'):
        super().__init__(message, path_route, path_message)

class RequiresLoginException(Message_Redirection_Exception):
    def __init__(self, message='Debes haber iniciado sesión para acceder a esta acción.', path_route='/', path_message='Inicia sesión'):
        super().__init__(message, path_route, path_message)

class LoginExpired(Message_Redirection_Exception):
    def __init__(self, message='Tu sesión ha expirado. Vuelve a iniciar sesion para continuar navegando.', path_route='/', path_message='Inicia sesión otra vez'):
        super().__init__(message, path_route, path_message)

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
            raise LoginExpired()
        except jwt.JWTError as e:
            raise RequiresLoginException()
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
    
    def registrar_usuario(self, usuario: Usuario, tipo : str):
        usuario.contraseña = self.get_hash_password(usuario.contraseña)
        if tipo == 'admin': 
            if Administradores.find_one({'cedula': usuario.cedula}): 
                return 'No se puede registrar si la cédula ya existe'
            if Administradores.insert_one(dict(usuario)).inserted_id: 
                return {'data': usuario, 'respuesta': 'Usuario registrado exitósamente. ADVERTENCIA: ESTA ES LA ÚLTIMA VEZ QUE VERÁ SU CONTRASEÑA LIBREMENTE'}
            else: return 'No se pudo registrar el administrador'
        elif tipo == 'cliente': 
            if Jugadores.find_one({'cedula': usuario.cedula}): 
                return 'No se puede registrar si la cédula ya existe'
            if Jugadores.insert_one(dict(usuario)).inserted_id: 
                return {'data': usuario, 'respuesta': 'Usuario registrado exitósamente. ADVERTENCIA: ESTA ES LA ÚLTIMA VEZ QUE VERÁ SU CONTRASEÑA LIBREMENTE'}
            else: return 'No se pudo registrar el cliente'
        return 'Hubo un problema y no se pudo registrar el usuario'



    async def authenticate_user(self, cedula: str, contraseña: str, tipo : str):
        try:
            usuario = obtener_usuario(cedula, tipo)
            if usuario: 
                password_check = self.verify_password(contraseña, usuario.contraseña)
                if password_check: 
                # if contraseña == usuario.contraseña: 
                    return usuario
                else: 
                    return False
                #return password_check #Nuestro código original retornaba el usuario (?)
                #por una buena razon lo retornaba
            else: 
                return False
        except:
            raise RequiresLoginException()

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
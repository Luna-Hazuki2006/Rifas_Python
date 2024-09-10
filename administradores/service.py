from bd import Administradores
from administradores.schemas import Administrador

def registrar_administradores(admin : Administrador): 
    if Administradores.insert_one(dict(admin)).inserted_id: 
        return admin
    else: return 'No se pudo registrar el administrador'

def listar_administradores(): 
    lista = Administradores.find({})
    return lista

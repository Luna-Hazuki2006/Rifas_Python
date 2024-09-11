from bd import Rifas
from Rifa.schemas import Rifa

def registrar_rifas(rifa : Rifa): 
    if Rifas.insert_one(dict(rifa)).inserted_id: 
        return rifa
    else: return 'No se pudo registrar la rifa'

def listar_rifas(): 
    lista = Rifas.find({})
    return lista

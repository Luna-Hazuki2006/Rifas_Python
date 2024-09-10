from bd import Jugadores
from cliente.schemas import Cliente

def registrar_jugador(cliente : Cliente): 
    if Jugadores.insert_one(dict(cliente)).inserted_id: 
        return cliente
    else: return 'No se pudo registrar el cliente'

def listar_jugadores(): 
    lista = Jugadores.find({})
    return lista

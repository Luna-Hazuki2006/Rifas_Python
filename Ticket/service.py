from bd import Tickets, Rifas
from Ticket.schemas import Ticket
from Rifa.schemas import Rifa
from Rifa.service import buscar_rifa

def registrar_Tickets(ticket : Ticket): 
    if Tickets.insert_one(dict(ticket)).inserted_id: 
        return ticket
    else: return 'No se pudo registrar la Ticket'

def listar_Tickets(): 
    lista = Tickets.find({})
    return lista

def listar_tickets_rifa(rifa : str):
    lista = [] 
    for esto in Tickets.find({'rifa': rifa}): 
        uno = Ticket(
            rifa=esto['rifa'], 
            numero=esto['numero'],  
            estatus=esto['estatus'], 
            ganador=esto['ganador']
        )
        lista.append(uno)
    return lista

def comprar_ticket(rifa : str, numero : int, cedula : str): 
    actual = Rifas.find_one({'codigo': rifa})
    if actual == None: return 'No se pudo encontrar una rifa con tal código'
    actual = buscar_rifa(rifa)
    compra = {}
    for esto in actual.tickets: 
        if esto['numero'] == numero: 
            esto['estatus'] = cedula
            compra = esto
            break
    if not cedula in actual.participantes: 
        actual.participantes.append(cedula)
    Rifas.replace_one({'codigo': rifa}, dict(actual))
    return compra

def buscar_comprados(rifa : str, cedula : str): 
    lista = []
    actual = Rifas.find_one({'codigo': rifa})
    if actual == None: return 'No se pudo encontrar una rifa con tal codigo'
    actual = buscar_rifa(rifa)
    for esto in actual.tickets: 
        if esto['estatus'] == cedula: 
            lista.append(esto)
    return lista
from bd import Tickets
from Ticket.schemas import Ticket

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
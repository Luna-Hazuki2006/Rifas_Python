from bd import Rifas, Tickets
from Rifa.schemas import Rifa
from Ticket.schemas import Ticket
from datetime import datetime
import random

def registrar_rifas(rifa : Rifa): 
    if Rifas.find_one({'codigo' : rifa.codigo}): 
        return 'Ese código ya existe, ¡intente otro!'
    for i in range(rifa.primer_numero, rifa.cantidad_tickets + rifa.primer_numero): 
        ticket = Ticket(numero=i)
        rifa.tickets.append(dict(ticket))
    if Rifas.insert_one(dict(rifa)).inserted_id: 
            # if Tickets.insert_one(dict(ticket)).inserted_id: continue
            # return 'Hubo un problema en la creación de tickets'
        return rifa
    return 'No se pudo registrar la rifa'

def listar_rifas(): 
    lista = Rifas.find({})
    return lista

def listar_rifas_actuales(): 
    hoy = datetime.now()
    lista = []
    for esto in Rifas.find({}): 
        if hoy < esto['final']: 
            lista.append(buscar_rifa(esto['codigo']))
    return lista 

def buscar_rifa(codigo : str): 
    este = Rifas.find_one({'codigo': codigo})
    este = Rifa(
        codigo=este['codigo'], 
        premio=este['premio'], 
        inicio=este['inicio'], 
        final=este['final'], 
        cantidad_tickets=este['cantidad_tickets'], 
        primer_numero=este['primer_numero'], 
        sorteo=este['sorteo'], 
        monto_renta=este['monto_renta'], 
        tickets=este['tickets']
    )
    return este

def revisar_codigo(codigo : str): 
    if Rifas.find_one({'codigo' : codigo}): return False
    return True
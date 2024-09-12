from bd import Rifas, Tickets
from Rifa.schemas import Rifa
from Ticket.schemas import Ticket
import random

def registrar_rifas(rifa : Rifa): 
    if Rifas.find_one({'codigo' : rifa.codigo}): 
        return 'Ese código ya existe, ¡intente otro!'
    if Rifas.insert_one(dict(rifa)).inserted_id: 
        ganador = random.randint(rifa.primer_numero, rifa.cantidad_tickets)
        for i in range(rifa.primer_numero, rifa.cantidad_tickets + 1): 
            ticket = Ticket(
                rifa=rifa.codigo, 
                numero=i, 
                estatus=False, 
                ganador=(True if ganador == i else False)
            )
            if Tickets.insert_one(dict(ticket)).inserted_id: continue
            return 'Hubo un problema en la creación de tickets'
        return rifa
    return 'No se pudo registrar la rifa'

def listar_rifas(): 
    lista = Rifas.find({})
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
        monto_renta=este['monto_renta']
    )
    return este

def revisar_codigo(codigo : str): 
    if Rifas.find_one({'codigo' : codigo}): return False
    return True
from fastapi import APIRouter, Request
from Ticket.schemas import Ticket
import Ticket.service as servicio
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_Tickets(request : Request): 
    lista = servicio.listar_Tickets()
    return lista

@router.get('/rifa/{rifa}')
async def listar_Ticket_rifa(request : Request, rifa : str): 
    esto = servicio.listar_tickets_rifa(rifa)
    return esto

@router.post('/{rifa}')
async def comprar_ticket(request : Request, rifa : str, numero : int, cedula : str): 
    esto = servicio.comprar_ticket(rifa, numero, cedula)
    return esto
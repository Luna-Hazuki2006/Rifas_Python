from fastapi import APIRouter, Request, Form, Depends
from Ticket.schemas import Ticket, Comprado
from typing import Annotated
import Ticket.service as servicio
from fastapi.templating import Jinja2Templates
from datetime import datetime
import Rifa.service as rifadas
from login.login import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()

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
async def comprar_ticket(request : Request, rifa : str, compra : Annotated[Comprado, Form()], info = Depends(auth_handler.auth_wrapper)): 
    esto = servicio.comprar_ticket(rifa, compra.numero, compra.cedula)
    lista = rifadas.buscar_rifa(rifa)
    return templates.TemplateResponse('rifa.html', {
        'request': request, 'rifa': lista, 'info': info})
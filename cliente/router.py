from fastapi import APIRouter, Request
from cliente.schemas import Cliente
import cliente.service as servicio
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_clientes(request : Request): 
    lista = await servicio.listar_jugadores()
    return lista
    # return templates.TemplateResponse('principal.html', {
    #     'request': request, 'lista': lista
    # })

@router.post('')
async def registrar_cliente(request : Request, cliente : Cliente): 
    esto = await servicio.registrar_jugador(cliente)
    return esto
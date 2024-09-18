from fastapi import APIRouter, Request, Response, Form
from typing import Annotated
from cliente.schemas import Cliente
import cliente.service as servicio
from fastapi.templating import Jinja2Templates
from login.login import Inicio, AuthHandler
from datetime import datetime

router = APIRouter()

auth_handler = AuthHandler()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_clientes(request : Request): 
    lista = servicio.listar_jugadores()
    return lista
    # return templates.TemplateResponse('principal.html', {
    #     'request': request, 'lista': lista
    # })

@router.post('')
async def registrar_cliente(request : Request, cliente : Annotated[Cliente, Form()]): 
    esto = servicio.registrar_jugador(cliente)
    return esto

@router.post('/iniciar')
async def iniciar_sesion(request : Request, data : Annotated[Inicio, Form()]): 
    pass
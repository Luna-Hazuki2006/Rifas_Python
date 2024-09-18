from fastapi import APIRouter, Request, Form
from typing import Annotated
from administradores.schemas import Administrador
import administradores.service as servicio
from fastapi.templating import Jinja2Templates
from login.login import Inicio, AuthHandler
from datetime import datetime

router = APIRouter()

auth_handler = AuthHandler()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_administradores(request : Request): 
    lista = servicio.listar_administradores()
    return lista
    # return templates.TemplateResponse('principal.html', {
    #     'request': request, 'lista': lista
    # })

@router.post('')
async def registrar_administrador(request : Request, admin : Annotated[Administrador, Form()]): 
    esto = servicio.registrar_administradores(admin)
    return esto

@router.post('/iniciar')
async def iniciar_sesion(request : Request, data : Annotated[Inicio, Form()]): 
    pass
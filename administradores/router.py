from fastapi import APIRouter, Request
from administradores.schemas import Administrador
import administradores.service as servicio
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_administradores(request : Request): 
    lista = servicio.listar_administradores()
    return lista
    # return templates.TemplateResponse('principal.html', {
    #     'request': request, 'lista': lista
    # })

@router.post('')
async def registrar_administrador(request : Request, admin : Administrador): 
    esto = servicio.registrar_administradores(admin)
    return esto
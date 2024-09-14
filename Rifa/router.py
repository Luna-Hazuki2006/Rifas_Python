from fastapi import APIRouter, Request, Form
from typing import Annotated
from Rifa.schemas import Rifa
import Rifa.service as servicio
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_rifas(request : Request): 
    lista = servicio.listar_rifas()
    return lista

@router.get('/actuales')
async def buscar_actuales(request : Request): 
    return servicio.listar_rifas_actuales()

@router.get('/revision/{codigo}')
async def revisar_rifa(request : Request, codigo : str): 
    return servicio.revisar_codigo(codigo)

@router.post('')
async def registrar_rifa(request : Request, rifa : Annotated[Rifa, Form()]):
    esto = servicio.registrar_rifas(rifa)
    return esto

@router.post('/entrar')
async def buscar_rifa(request : Request, codigo : Annotated[str, Form()]): 
    rifa = servicio.buscar_rifa(codigo)
    return templates.TemplateResponse('index.html', {
        'request': request, 'rifa': rifa})
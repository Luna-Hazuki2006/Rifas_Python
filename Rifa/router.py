from fastapi import APIRouter, Request, Form, Depends
from typing import Annotated
from Rifa.schemas import Rifa
import Rifa.service as servicio
from fastapi.templating import Jinja2Templates
from login.login import AuthHandler
from datetime import datetime

router = APIRouter()

auth_handler = AuthHandler()

templates = Jinja2Templates(directory="./templates")

@router.get('')
async def listar_rifas(request : Request): 
    lista = servicio.listar_rifas()
    return lista

@router.get('/actuales')
async def buscar_actuales(request : Request): 
    return servicio.listar_rifas_actuales()

@router.get('/{codigo}')
async def buscar_este(request : Request, codigo : str, info = Depends(auth_handler.auth_wrapper)): 
    hoy = datetime.now()
    esto = servicio.buscar_rifa(codigo)
    sorteo = esto.sorteo
    return templates.TemplateResponse('rifa.html', {
        'request': request, 'rifa': esto, 'hoy': hoy, 'sorteo': sorteo, 'token': info})

@router.get('/revision/{codigo}')
async def revisar_rifa(request : Request, codigo : str): 
    return servicio.revisar_codigo(codigo)

@router.get('/tiempo/{tiempo}')
async def obtener_tiempo(tiempo : datetime): 
    return servicio.buscar_tiempo(tiempo)

@router.post('')
async def registrar_rifa(request : Request, rifa : Annotated[Rifa, Form()], info = Depends(auth_handler.auth_wrapper)):
    esto = servicio.registrar_rifas(rifa)
    return templates.TemplateResponse('rifa.html', {
        'request': request, 'rifa': esto, 'token': info})

@router.post('/entrar')
async def buscar_rifa(request : Request, codigo : Annotated[str, Form()], info = Depends(auth_handler.auth_wrapper)): 
    hoy = datetime.now()
    rifa = servicio.buscar_rifa(codigo)
    sorteo = rifa.sorteo
    return templates.TemplateResponse('rifa.html', {
        'request': request, 'rifa': rifa, 'hoy': hoy, 'sorteo': sorteo, 'token': info})

@router.post('/sortear/{codigo}')
async def sortear_rifa(request : Request, codigo : str, info = Depends(auth_handler.auth_wrapper)): 
    rifa = servicio.sortear_rifa(codigo)
    return templates.TemplateResponse('rifa.html', {
        'request': request, 'rifa': rifa, 'token': info})
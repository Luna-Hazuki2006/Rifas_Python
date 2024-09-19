from fastapi import APIRouter, Request, Form, Response
from typing import Annotated
from administradores.schemas import Administrador
import administradores.service as servicio
from fastapi.templating import Jinja2Templates
from login.login import Inicio, AuthHandler
import Rifa.service as rifas
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
async def iniciar_sesion(request : Request, response : Response, data : Annotated[Inicio, Form()]): 
    esto = await auth_handler.authenticate_user(data.cedula, data.contraseña, 'admin')
    completo = f'{esto.nombre} {esto.apellido}'
    atoken = auth_handler.create_access_token(data={'cedula': esto.cedula, 'nombre_completo': completo, 'tipo': 'admin', 'correo': esto.correo})
    response.set_cookie(key="Authorization", value= f"{atoken}", httponly=True)
    lista = rifas.listar_rifas_actuales()
    return templates.TemplateResponse('index.html', {
        'request': request, 'rifas': lista, 'verdad': True})
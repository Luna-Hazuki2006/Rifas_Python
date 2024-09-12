from fastapi import APIRouter, Request, Form
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

@router.get('/{codigo}')
async def buscar_rifa(request : Request, codigo : str): 
    return servicio.buscar_rifa(codigo)

@router.get('/revision/{codigo}')
async def buscar_rifa(request : Request, codigo : str): 
    return servicio.revisar_codigo(codigo)

@router.post('')
async def registrar_rifa(request : Request, 
                         codigo : str = Form(...), 
                         premio : str = Form(...), 
                         inicio : datetime = Form(...), 
                         final : datetime = Form(...), 
                         cantidad_tickets : int = Form(...), 
                         primer_numero : int = Form(...), 
                         sorteo : datetime = Form(...), 
                         monto_renta : float = Form(...)):
    rifa = Rifa(
        codigo=codigo, 
        premio=premio, 
        inicio=inicio, 
        final=final, 
        cantidad_tickets=cantidad_tickets, 
        primer_numero=primer_numero, 
        sorteo=sorteo, 
        monto_renta=monto_renta
    ) 
    esto = servicio.registrar_rifas(rifa)
    return esto
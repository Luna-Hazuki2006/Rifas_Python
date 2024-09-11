from fastapi import APIRouter, Request
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

@router.post('')
async def registrar_rifa(request : Request, rifa : Rifa): 
    esto = servicio.registrar_rifas(Rifa)
    return esto
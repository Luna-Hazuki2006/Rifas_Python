from pydantic import BaseModel, EmailStr
from datetime import datetime

class Rifa(BaseModel): 
    codigo : str
    premio : str
    creador : str
    inicio : datetime
    final : datetime
    cantidad_tickets : int
    primer_numero : int
    sorteo : datetime
    monto_venta : float
    participantes : list[str] = []
    tickets : list[dict] = []
    ganado : bool = False

class EmailSchema(BaseModel):
    email: list[EmailStr]
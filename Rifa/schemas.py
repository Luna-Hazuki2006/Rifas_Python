from pydantic import BaseModel
from datetime import datetime

class Rifa(BaseModel): 
    codigo : str
    premio : str
    inicio : datetime
    final : datetime
    cantiddad_tickets : int
    primer_numero : int
    sorteo : datetime
    monto_renta : float
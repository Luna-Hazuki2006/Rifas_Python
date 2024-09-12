from pydantic import BaseModel

class Ticket(BaseModel):
    rifa :  str
    numero : int
    estatus : bool
    ganador : bool
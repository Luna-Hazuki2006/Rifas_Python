from pydantic import BaseModel

class Ticket(BaseModel): 
    numero : int
    estatus : bool
    ganador : bool
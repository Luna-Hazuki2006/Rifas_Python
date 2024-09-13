from pydantic import BaseModel
from typing import Union

class Ticket(BaseModel):
    numero : int
    estatus : Union[bool, str] = False
    ganador : bool = False

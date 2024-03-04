from typing import Optional
from pydantic import BaseModel

class IDES(BaseModel):
    id: Optional[int] = None
    nome: str
    versao: int
    linguagem: str
    
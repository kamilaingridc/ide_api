from typing import Optional
from pydantic import Basemodel
# importação das bibliotecas

class IDES (Basemodel):
    id: Optional[int] = None
    nome: str
    versao: int
    linguagem: str

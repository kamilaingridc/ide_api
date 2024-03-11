from pydantic import BaseModel

class IDES(BaseModel):
    id: str | None = None
    nome: str | None = None
    versao: float | None = None
    linguagem: str | None = None
    imagem: str | None = None
    
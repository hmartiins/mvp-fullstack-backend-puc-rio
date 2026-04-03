from typing import List
from pydantic import BaseModel


class ErroResponse(BaseModel):
    erro: str


class ErrosResponse(BaseModel):
    erros: List[str]


class MensagemResponse(BaseModel):
    mensagem: str

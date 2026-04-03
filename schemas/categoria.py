from typing import Optional, Annotated, List
from pydantic import BaseModel, Field


class CategoriaInput(BaseModel):
    nome: Annotated[str, Field(min_length=1, description="Nome da categoria")]
    descricao: Optional[str] = Field(None, description="Descrição opcional")


class CategoriaResponse(BaseModel):
    id: str
    nome: str
    descricao: Optional[str] = None


class CategoriaListResponse(BaseModel):
    root: List[CategoriaResponse]


class CategoriaPath(BaseModel):
    categoria_id: str = Field(description="UUID da categoria")

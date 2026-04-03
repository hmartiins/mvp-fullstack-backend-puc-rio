from typing import Optional
from pydantic import BaseModel, Field
from typing import Annotated


class CategoriaInput(BaseModel):
    nome: Annotated[str, Field(min_length=1)]
    descricao: Optional[str] = None

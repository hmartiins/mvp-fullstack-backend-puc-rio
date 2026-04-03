from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class DespesaInput(BaseModel):
    descricao: Annotated[str, Field(min_length=1, description="Descrição da despesa")]
    valor: Annotated[float, Field(gt=0, description="Valor positivo")]
    data: str = Field(description="Data no formato YYYY-MM-DD")
    categoria_id: Annotated[str, Field(min_length=1, description="UUID da categoria")]

    @field_validator("data")
    @classmethod
    def validate_data_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("deve estar no formato YYYY-MM-DD")
        return v


class DespesaResponse(BaseModel):
    id: str
    descricao: str
    valor: float
    data: str
    categoria_id: str
    categoria_nome: Optional[str] = None


class ResumoResponse(BaseModel):
    categoria_id: str
    categoria_nome: str
    total: float
    quantidade: int


class DespesaPath(BaseModel):
    despesa_id: str = Field(description="UUID da despesa")


class PeriodoQuery(BaseModel):
    data_inicio: str = Field(description="Data início no formato YYYY-MM-DD")
    data_fim: str = Field(description="Data fim no formato YYYY-MM-DD")

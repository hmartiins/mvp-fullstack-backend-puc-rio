from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class DespesaInput(BaseModel):
    descricao: Annotated[str, Field(min_length=1)]
    valor: Annotated[float, Field(gt=0)]
    data: str
    categoria_id: Annotated[str, Field(min_length=1)]

    @field_validator("data")
    @classmethod
    def validate_data_format(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("deve estar no formato YYYY-MM-DD")
        return v

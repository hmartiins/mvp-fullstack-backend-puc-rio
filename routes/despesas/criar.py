from flask import jsonify

from schemas.despesa import DespesaInput, DespesaResponse
from schemas.comum import ErroResponse, ErrosResponse
from service import despesa_service
from utils import parse_date
from routes.despesas import bp


@bp.post(
    "",
    responses={"201": DespesaResponse, "404": ErroResponse, "422": ErrosResponse},
)
def criar_despesa(body: DespesaInput):
    """Cadastrar nova despesa"""
    despesa = despesa_service.criar(
        descricao=body.descricao.strip(),
        valor=body.valor,
        data=parse_date(body.data),
        categoria_id=body.categoria_id,
    )
    return jsonify(despesa.to_dict()), 201

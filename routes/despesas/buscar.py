from flask import jsonify

from schemas.despesa import DespesaPath, DespesaResponse
from schemas.comum import ErroResponse
from service import despesa_service
from routes.despesas import bp


@bp.get("/<despesa_id>", responses={"200": DespesaResponse, "404": ErroResponse})
def buscar_despesa(path: DespesaPath):
    """Buscar despesa pelo ID"""
    despesa = despesa_service.buscar(path.despesa_id)
    return jsonify(despesa.to_dict()), 200

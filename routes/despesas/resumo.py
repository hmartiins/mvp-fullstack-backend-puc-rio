from flask import jsonify

from schemas.despesa import ResumoResponse
from schemas.comum import ErroResponse
from service import despesa_service
from routes.despesas import bp


@bp.get("/resumo", responses={"200": ResumoResponse, "500": ErroResponse})
def resumo_despesas():
    """Total gasto agrupado por categoria"""
    return jsonify(despesa_service.resumo()), 200

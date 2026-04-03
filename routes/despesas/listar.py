from flask import jsonify

from schemas.despesa import DespesaResponse
from service import despesa_service
from routes.despesas import bp


@bp.get("", responses={"200": DespesaResponse})
def listar_despesas():
    """Listar todas as despesas"""
    return jsonify([d.to_dict() for d in despesa_service.listar()]), 200

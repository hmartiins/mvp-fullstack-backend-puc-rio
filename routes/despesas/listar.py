from flask import jsonify

from model.models import Despesa
from schemas.despesa import DespesaResponse
from schemas.comum import ErroResponse
from routes.despesas import bp


@bp.get("", responses={"200": DespesaResponse, "500": ErroResponse})
def listar_despesas():
    """Listar todas as despesas"""
    try:
        despesas = Despesa.query.order_by(Despesa.data.desc(), Despesa.id.desc()).all()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesas", "detalhe": str(e)}), 500

    return jsonify([d.to_dict() for d in despesas]), 200

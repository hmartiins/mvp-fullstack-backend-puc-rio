from flask import jsonify

from model.models import db, Despesa
from schemas.despesa import DespesaPath, DespesaResponse
from schemas.comum import ErroResponse
from routes.despesas import bp


@bp.get("/<despesa_id>", responses={"200": DespesaResponse, "404": ErroResponse})
def buscar_despesa(path: DespesaPath):
    """Buscar despesa pelo ID"""
    try:
        despesa = db.session.get(Despesa, path.despesa_id)
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesa", "detalhe": str(e)}), 500

    if not despesa:
        return jsonify({"erro": "Despesa não encontrada"}), 404

    return jsonify(despesa.to_dict()), 200

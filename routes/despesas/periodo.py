from flask import jsonify

from model.models import Despesa
from schemas.despesa import DespesaResponse, PeriodoQuery
from schemas.comum import ErroResponse
from utils import parse_date
from routes.despesas import bp


@bp.get("/periodo", responses={"200": DespesaResponse, "400": ErroResponse})
def despesas_por_periodo(query: PeriodoQuery):
    """Filtrar despesas por intervalo de datas"""
    try:
        di = str(parse_date(query.data_inicio))
        df = str(parse_date(query.data_fim))
    except ValueError:
        return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    if di > df:
        return jsonify({"erro": "'data_inicio' não pode ser posterior a 'data_fim'"}), 400

    try:
        despesas = (
            Despesa.query
            .filter(Despesa.data.between(di, df))
            .order_by(Despesa.data.asc())
            .all()
        )
    except Exception as e:
        return jsonify({"erro": "Erro ao filtrar despesas", "detalhe": str(e)}), 500

    return jsonify([d.to_dict() for d in despesas]), 200

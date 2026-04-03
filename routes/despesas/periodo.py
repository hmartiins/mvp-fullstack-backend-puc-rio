from flask import jsonify

from schemas.despesa import DespesaResponse, PeriodoQuery
from schemas.comum import ErroResponse
from service import despesa_service
from utils import parse_date
from routes.despesas import bp


@bp.get("/periodo", responses={"200": DespesaResponse, "400": ErroResponse})
def despesas_por_periodo(query: PeriodoQuery):
    """Filtrar despesas por intervalo de datas"""
    try:
        data_inicio = parse_date(query.data_inicio)
        data_fim = parse_date(query.data_fim)
    except ValueError:
        return jsonify({"erro": "Datas devem estar no formato YYYY-MM-DD"}), 400

    despesas = despesa_service.por_periodo(data_inicio, data_fim)
    return jsonify([d.to_dict() for d in despesas]), 200

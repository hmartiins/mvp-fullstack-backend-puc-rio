from flask import request, jsonify

from model.models import Despesa
from utils import parse_date
from routes.despesas import bp


@bp.route("/periodo", methods=["GET"])
def despesas_por_periodo():
    """
    Filtrar despesas por intervalo de datas
    ---
    tags:
      - Despesas
    parameters:
      - in: query
        name: data_inicio
        type: string
        required: true
        description: Data de início no formato YYYY-MM-DD
        example: "2024-01-01"
      - in: query
        name: data_fim
        type: string
        required: true
        description: Data de fim no formato YYYY-MM-DD
        example: "2024-12-31"
    responses:
      200:
        description: Despesas no período informado
        schema:
          type: array
          items:
            $ref: '#/definitions/Despesa'
      400:
        description: Parâmetros inválidos
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    data_inicio = request.args.get("data_inicio", "").strip()
    data_fim = request.args.get("data_fim", "").strip()

    if not data_inicio or not data_fim:
        return jsonify({"erro": "Os parâmetros 'data_inicio' e 'data_fim' são obrigatórios"}), 400

    try:
        di = str(parse_date(data_inicio))
        df = str(parse_date(data_fim))
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

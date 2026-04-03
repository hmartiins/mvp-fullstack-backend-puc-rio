from flask import request, jsonify

from models import get_db
from utils import parse_date, row_to_dict
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
        conn = get_db()
        rows = conn.execute(
            """
            SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id, c.nome AS categoria_nome
            FROM despesas d
            JOIN categorias c ON c.id = d.categoria_id
            WHERE d.data BETWEEN ? AND ?
            ORDER BY d.data ASC
            """,
            (di, df),
        ).fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao filtrar despesas", "detalhe": str(e)}), 500

    return jsonify([row_to_dict(r) for r in rows]), 200

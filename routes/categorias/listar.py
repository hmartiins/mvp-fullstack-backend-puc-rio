from flask import jsonify

from models import get_db
from utils import row_to_dict
from routes.categorias import bp


@bp.route("", methods=["GET"])
def listar_categorias():
    """
    Listar todas as categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias
        schema:
          type: array
          items:
            $ref: '#/definitions/Categoria'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT id, nome, descricao FROM categorias ORDER BY nome"
        ).fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar categorias", "detalhe": str(e)}), 500

    return jsonify([row_to_dict(r) for r in rows]), 200

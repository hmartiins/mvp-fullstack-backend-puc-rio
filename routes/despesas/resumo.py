from flask import jsonify
from sqlalchemy import func

from model.models import db, Categoria, Despesa
from routes.despesas import bp


@bp.route("/resumo", methods=["GET"])
def resumo_despesas():
    """
    Total gasto agrupado por categoria
    ---
    tags:
      - Despesas
    responses:
      200:
        description: Resumo com total e quantidade de despesas por categoria
        schema:
          type: array
          items:
            $ref: '#/definitions/Resumo'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        rows = (
            db.session.query(
                Categoria.id.label("categoria_id"),
                Categoria.nome.label("categoria_nome"),
                func.round(func.coalesce(func.sum(Despesa.valor), 0), 2).label("total"),
                func.count(Despesa.id).label("quantidade"),
            )
            .outerjoin(Despesa, Despesa.categoria_id == Categoria.id)
            .group_by(Categoria.id, Categoria.nome)
            .order_by(func.sum(Despesa.valor).desc())
            .all()
        )
    except Exception as e:
        return jsonify({"erro": "Erro ao gerar resumo", "detalhe": str(e)}), 500

    return jsonify([
        {
            "categoria_id": r.categoria_id,
            "categoria_nome": r.categoria_nome,
            "total": r.total,
            "quantidade": r.quantidade,
        }
        for r in rows
    ]), 200

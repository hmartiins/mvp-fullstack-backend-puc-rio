from flask import jsonify
from sqlalchemy import func

from model.models import db, Categoria, Despesa
from schemas.despesa import ResumoResponse
from schemas.comum import ErroResponse
from routes.despesas import bp


@bp.get("/resumo", responses={"200": ResumoResponse, "500": ErroResponse})
def resumo_despesas():
    """Total gasto agrupado por categoria"""
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

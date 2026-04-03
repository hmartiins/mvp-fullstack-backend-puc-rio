import uuid

from flask import jsonify

from model.models import db, Categoria, Despesa
from schemas.despesa import DespesaInput, DespesaResponse
from schemas.comum import ErroResponse, ErrosResponse
from routes.despesas import bp


@bp.post(
    "",
    responses={"201": DespesaResponse, "404": ErroResponse, "422": ErrosResponse},
)
def criar_despesa(body: DespesaInput):
    """Cadastrar nova despesa"""
    try:
        categoria = db.session.get(Categoria, body.categoria_id)
        if not categoria:
            return jsonify({"erro": f"Categoria com id {body.categoria_id} não encontrada"}), 404

        despesa = Despesa(
            id=str(uuid.uuid4()),
            descricao=body.descricao.strip(),
            valor=body.valor,
            data=body.data,
            categoria_id=body.categoria_id,
        )
        db.session.add(despesa)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar despesa", "detalhe": str(e)}), 500

    return jsonify(despesa.to_dict()), 201

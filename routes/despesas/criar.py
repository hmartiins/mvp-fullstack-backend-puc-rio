import uuid

from flask import jsonify

from model.models import db, Categoria, Despesa
from schemas.despesa import DespesaInput
from utils import validate_body
from routes.despesas import bp


@bp.route("", methods=["POST"])
@validate_body(DespesaInput)
def criar_despesa(body: DespesaInput):
    """
    Cadastrar nova despesa
    ---
    tags:
      - Despesas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/DespesaInput'
    responses:
      201:
        description: Despesa criada com sucesso
        schema:
          $ref: '#/definitions/Despesa'
      400:
        description: Dados inválidos ou campos obrigatórios ausentes
        schema:
          $ref: '#/definitions/Erro'
      404:
        description: Categoria não encontrada
        schema:
          $ref: '#/definitions/Erro'
      422:
        description: Tipo de campo inválido
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
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

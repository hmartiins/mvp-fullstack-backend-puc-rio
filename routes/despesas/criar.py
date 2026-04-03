import uuid

from flask import request, jsonify

from model.models import db, Categoria, Despesa
from utils import parse_date
from routes.despesas import bp


@bp.route("", methods=["POST"])
def criar_despesa():
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
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"erro": "Corpo da requisição inválido ou ausente"}), 400

    campos_obrigatorios = ["descricao", "valor", "data", "categoria_id"]
    ausentes = [c for c in campos_obrigatorios if data.get(c) is None]
    if ausentes:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {', '.join(ausentes)}"}), 400

    descricao = str(data["descricao"]).strip()
    if not descricao:
        return jsonify({"erro": "O campo 'descricao' não pode estar vazio"}), 400

    try:
        valor = float(data["valor"])
        if valor <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"erro": "O campo 'valor' deve ser um número positivo"}), 400

    try:
        data_despesa = str(parse_date(str(data["data"])))
    except ValueError:
        return jsonify({"erro": "O campo 'data' deve estar no formato YYYY-MM-DD"}), 400

    categoria_id = str(data["categoria_id"]).strip()
    if not categoria_id:
        return jsonify({"erro": "O campo 'categoria_id' não pode estar vazio"}), 400

    try:
        categoria = db.session.get(Categoria, categoria_id)
        if not categoria:
            return jsonify({"erro": f"Categoria com id {categoria_id} não encontrada"}), 404

        despesa = Despesa(
            id=str(uuid.uuid4()),
            descricao=descricao,
            valor=valor,
            data=data_despesa,
            categoria_id=categoria_id,
        )
        db.session.add(despesa)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar despesa", "detalhe": str(e)}), 500

    return jsonify(despesa.to_dict()), 201

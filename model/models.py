from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    descricao = db.Column(db.String, nullable=True)

    despesas = db.relationship("Despesa", backref="categoria", lazy="select")

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}


class Despesa(db.Model):
    __tablename__ = "despesas"

    id = db.Column(db.String, primary_key=True)
    descricao = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.String, nullable=False)
    categoria_id = db.Column(db.String, db.ForeignKey("categorias.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
        }

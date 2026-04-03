from model.database import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    descricao = db.Column(db.String, nullable=True)

    despesas = db.relationship("Despesa", backref="categoria", lazy="select")

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}

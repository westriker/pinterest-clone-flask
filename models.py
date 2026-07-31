from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


# Tabela de Usuários (adicionado UserMixin)
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False, unique=True)
    email = database.Column(database.String(100), nullable=False, unique=True)
    senha = database.Column(database.String(100), nullable=False)
    foto_perfil = database.Column(database.String(100), default="default.png")

    fotos = database.relationship("Foto", backref="usuario", lazy=True)


# Tabela de Fotos
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(
        database.String(100), default="default.png", nullable=False
    )
    data_criacao = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow
    )
    id_usuario = database.Column(
        database.Integer, database.ForeignKey("usuario.id"), nullable=False
    )
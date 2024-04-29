# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    senha_hash = db.Column(db.String(256))  # Modificação aqui
    nivel_acesso = db.Column(db.String(50))

    def __init__(self, nome, sobrenome, email, senha, nivel_acesso):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.set_password(senha)
        self.nivel_acesso = nivel_acesso

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'nivel_acesso': self.nivel_acesso
        }

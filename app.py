from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/sistema_usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Define o tempo de expiração do token JWT
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='Sistema de Usuários', description='API para gerenciar usuários')
jwt = JWTManager(app)

user_fields = api.model('User', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True),
    'sobrenome': fields.String(required=True),
    'email': fields.String(required=True),
    'senha': fields.String(required=True),
    'nivel_acesso': fields.String(required=True)
})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    senha_hash = db.Column(db.String(256))
    nivel_acesso = db.Column(db.String(50))

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
            'senha': self.senha_hash,
            'nivel_acesso': self.nivel_acesso
        }

class UserList(Resource):
    @api.marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        user_list = [user.to_dict() for user in users]
        return user_list

    @jwt_required()  # Requer autenticação JWT para acessar este endpoint
    @api.expect(user_fields)
    @api.marshal_with(user_fields, code=201)
    def post(self):
        data = api.payload
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'E-mail já está em uso'}), 400
        new_user = User(
            nome=data['nome'],
            sobrenome=data['sobrenome'],
            email=data['email'],
            nivel_acesso=data['nivel_acesso']
        )
        new_user.set_password(data['senha'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

class UserResource(Resource):
    @api.marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @jwt_required()  # Requer autenticação JWT para acessar este endpoint
    @api.expect(user_fields)
    @api.marshal_with(user_fields)
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user.id != current_user_id:
            return {'message': 'Você só pode atualizar seu próprio usuário'}, 403
        data = api.payload
        if 'nome' in data:
            user.nome = data['nome']
        if 'sobrenome' in data:
            user.sobrenome = data['sobrenome']
        if 'email' in data:
            user.email = data['email']
        if 'nivel_acesso' in data:
            user.nivel_acesso = data['nivel_acesso']
        if 'senha' in data:
            user.set_password(data['senha'])
        db.session.commit()
        return user

    @jwt_required()  # Requer autenticação JWT para acessar este endpoint
    @api.response(204, 'Usuário deletado com sucesso')
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        if current_user.nivel_acesso != 'admin':
            return {'message': 'Apenas administradores podem excluir usuários'}, 403
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserRegister(Resource):
    # Não há autenticação JWT para esta rota
    @api.expect(user_fields)
    @api.response(201, 'Usuário registrado com sucesso')
    def post(self):
        data = api.payload
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'E-mail já está em uso'}), 400
        new_user = User(
            nome=data['nome'],
            sobrenome=data['sobrenome'],
            email=data['email'],
            nivel_acesso=data['nivel_acesso']
        )
        new_user.set_password(data['senha'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201  

class UserLogin(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        senha = data.get('senha')
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(senha):
            return {'message': 'E-mail ou senha inválidos'}, 401
        access_token = create_access_token(identity=user.id, additional_claims={'nivel_acesso': user.nivel_acesso})
        return {'access_token': access_token}

api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)

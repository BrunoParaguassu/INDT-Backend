# auth.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import User

def initialize_jwt(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        senha = data.get('senha')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(senha):
            return jsonify({'message': 'Credenciais inválidas'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user=user.to_dict())

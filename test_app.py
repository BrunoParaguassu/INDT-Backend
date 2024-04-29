import pytest
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_get_user(client):
    with app.app_context():
        user = User(nome='Teste', sobrenome='Testado', email='teste@teste.com', senha='123456', nivel_acesso='admin')
        db.session.add(user)
        db.session.commit()

    with app.app_context():
        response = client.get('/users/1')
        assert response.status_code == 200
        assert response.json['nome'] == 'Teste'  # Verifica se o nome do usuário está correto

def test_update_user(client):
    with app.app_context():
        user = User(nome='Teste', sobrenome='Testado', email='teste@teste.com', senha='123456', nivel_acesso='admin')
        db.session.add(user)
        db.session.commit()

    with app.app_context():
        response = client.put('/users/1', json={'nome': 'Novo Nome'})
        assert response.status_code == 200

        # Verifica se o nome do usuário foi atualizado corretamente
        updated_user = User.query.get(1)
        assert updated_user.nome == 'Novo Nome'

def test_delete_user(client):
    with app.app_context():
        user = User(nome='Teste', sobrenome='Testado', email='teste@teste.com', senha='123456', nivel_acesso='admin')
        db.session.add(user)
        db.session.commit()

    with app.app_context():
        response = client.delete('/users/1')
        assert response.status_code == 204

        # Verifica se o usuário foi excluído corretamente
        deleted_user = User.query.get(1)
        assert deleted_user is None

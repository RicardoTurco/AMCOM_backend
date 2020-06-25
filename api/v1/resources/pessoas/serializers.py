from api.v1 import api
from flask_restplus import fields


pessoa = api.model('Pessoa', {
    'idpessoa': fields.String(readonly=True, description='Pessoa ID'),
    'nome': fields.String(readonly=True, description='Nome da Pessoa'),
    'cpf': fields.String(readonly=True, description='CPF da Pessoa'),
    'datanascimento': fields.Date(readonly=True, description='Dt.Nasct da Pessoa'),
    'username': fields.String(readonly=True, description='UserName da Pessoa'),
    'email': fields.String(readonly=True, description='Email da Pessoa')
})

create_pessoa = api.model('Pessoa', {
    'nome': fields.String(readonly=True, description='Nome da Pessoa'),
    'cpf': fields.String(readonly=True, description='CPF da Pessoa'),
    'datanascimento': fields.String(readonly=True, description='Dt.Nasct da Pessoa'),
    'username': fields.String(readonly=True, description='UserName da Pessoa'),
    'email': fields.String(readonly=True, description='Email da Pessoa'),
    'password': fields.String(readonly=True, description='Password da Pessoa')
})

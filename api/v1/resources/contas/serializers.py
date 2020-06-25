from api.v1 import api
from flask_restplus import fields


conta_all = api.model('Conta', {
    'idconta': fields.String(readonly=True, description='Conta ID'),
    'tipoconta': fields.String(readonly=True, description='Tipo Conta'),
    'nome': fields.String(readonly=True, description='Nome Pessoa'),
    'saldo': fields.Float(readonly=True, description='Saldo of Conta'),
    'limitesaquediario': fields.Float(readonly=True, description='Limite Saque Diario'),
    'flagativo': fields.Boolean(readonly=True, description='If Conta is active'),
    'datacriacao': fields.Date(readonly=True, description='Data criacao conta')
})

create_conta = api.model('Conta', {
    'idpessoa': fields.String(readonly=True, description='Pessoa ID'),
    'saldo': fields.Float(readonly=True, description='Saldo of Conta'),
    'limitesaquediario': fields.Float(readonly=True, description='Limite Saque Diario'),
    'idtipoconta': fields.String(readonly=True, description='Tipo Conta ID'),
    'flagativo': fields.Boolean(readonly=True, description='If Conta is active'),
    'datacriacao': fields.String(readonly=True, description='Data criacao conta')
})

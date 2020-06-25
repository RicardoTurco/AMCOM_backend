from api.v1 import api
from flask_restplus import fields


transacao_op = api.model('Transacao', {
    'idtransacao': fields.String(readonly=True, description='Transacao ID'),
    'idconta': fields.String(readonly=True, description='Tipo Conta ID'),
    'tipotransacao': fields.String(readonly=True, description='Tipo Transacao'),
    'operacao': fields.String(readonly=True, description='Operacao (D, C)'),
    'valor': fields.Float(readonly=True, description='Valor transacao'),
    'datatransacao': fields.Date(readonly=True, description='Data transacao')
})

create_transacao = api.model('Transacao', {
    'idconta': fields.String(readonly=True, description='Tipo Conta ID'),
    'idtipotransacao': fields.String(readonly=True, description='Tipo Transacao ID'),
    'valor': fields.Float(readonly=True, description='Valor transacao'),
    'datatransacao': fields.String(readonly=True, description='Data transacao')
})

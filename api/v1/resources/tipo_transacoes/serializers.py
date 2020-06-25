from api.v1 import api
from flask_restplus import fields


tipo_transacao = api.model('TipoTransacao', {
    'idtipotransacao': fields.String(readonly=True, description='Tipo Transacao ID'),
    'tipotransacao': fields.String(readonly=True, description='Tipo Transacao'),
    'operacao': fields.String(readonly=True, description='D ou C')
})

create_tipo_transacao = api.model('TipoTransacao', {
    'tipotransacao': fields.String(readonly=True, description='Tipo Transacao'),
    'operacao': fields.String(readonly=True, description='D ou C')
})
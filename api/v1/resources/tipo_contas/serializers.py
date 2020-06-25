from api.v1 import api
from flask_restplus import fields


tipo_conta = api.model('TipoConta', {
    'idtipoconta': fields.String(readonly=True, description='Tipo Conta ID'),
    'tipoconta': fields.String(readonly=True, description='Tipo Conta')
})

create_tipo_conta = api.model('TipoConta', {
    'tipoconta': fields.String(readonly=True, description='Tipo Conta')
})

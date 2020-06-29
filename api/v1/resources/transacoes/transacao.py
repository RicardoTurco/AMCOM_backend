from flask_restplus import Resource, Namespace
from .serializers import transacao_op, create_transacao
from .models import Transacoes


api = Namespace('transacoes', 'Transacoes Endpoint')


@api.route('')
class TransacaoList(Resource):

    @api.marshal_list_with(transacao_op)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all transacoes
        """
        return Transacoes.get_all_transacoes(), 200

    @api.expect(create_transacao)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Inauthorized',
        422: 'Cannot create transacao',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new transacao
        """
        Transacoes.insert_transacao(api.payload)
        return {"msg": "Transacao created."}, 201


@api.route('/conta/<string:idconta>')
class TransacaoConta(Resource):

    @api.marshal_list_with(transacao_op)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Transacao not found',
        500: 'Internal Server Error'
    }, params={'idconta': 'Conta ID'})
    def get(self, idconta):
        """
        Get all transacoes of conta
        """
        transacoes = Transacoes.get_all_transacoes_conta(idconta)
        if not transacoes:
            api.abort(404, 'Transacao not found')
        return transacoes

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Transacao not found',
        500: 'Internal Server Error'
    }, params={'idconta': 'Conta ID'})
    def delete(self, idconta):
        """
        Delete all transacoes of conta
        """
        transacoes = Transacoes.get_all_transacoes_conta(idconta)
        if not transacoes:
            api.abort(303, 'Transacao not found')
        Transacoes.delete_transacoes_conta(transacoes)
        return {'msg': 'All Transacoes of Conta deleted.'}


@api.route('/id/<string:id>')
class TransacaoId(Resource):

    @api.marshal_with(transacao_op)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Transacao ID'})
    def get(self, id):
        """
        Get transacao by ID
        """
        transacao = Transacoes.get_transacao(id)
        if not transacao:
            api.abort(404, 'Transacao not found')
        return transacao, 200

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Transacao ID'})
    def delete(self, id):
        """
        Delete transacao by ID
        """
        transacao = Transacoes.get_transacao(id)
        if not transacao:
            api.abort(404, 'Transacao not found')

        Transacoes.delete_transacao(transacao)
        return {"msg": "Transacao deleted."}, 200

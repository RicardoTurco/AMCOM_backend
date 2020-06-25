from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import tipo_transacao, create_tipo_transacao
from .models import TipoTransacoes


api = Namespace('tipo-transacoes', 'Tipo Transacoes Endpoint')


@api.route('')
class TipoTransacaoList(Resource):

    @api.marshal_list_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    # @jwt_required
    def get(self):
        """
        Get all tipo transacoes
        """
        return TipoTransacoes.get_all_tipo_transacoes(), 200

    @api.expect(create_tipo_transacao)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'Tipo Transacao already exists',
        422: 'Cannot create tipo transacao',
        500: 'Internal Server Error'})
    # @jwt_required
    def post(self):
        """
        Creates a new tipo transacao
        """
        tipo_transacao_by_name = TipoTransacoes.get_tipo_transacao_nome(api.payload.get('tipotransacao'))
        if tipo_transacao_by_name:
            api.abort(409, 'Tipo Transacao already exists')

        TipoTransacoes.insert_tipo_transacao(api.payload)
        return {"msg": "Tipo Transacao created."}, 201


@api.route('/operacao/<string:operacao>')
class TipoTransacaoOperacao(Resource):

    @api.marshal_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'operacao': 'Operacao Tipo Transacao'})
    # @jwt_required
    def get(self, operacao):
        """
        Get tipo transacao by Operacao
        """
        tipo_transacoes = TipoTransacoes.get_tipo_transacao_operacao(operacao)
        if not tipo_transacoes:
            api.abort(404, 'Tipo Transacao not found')
        return tipo_transacoes, 200


@api.route('/nome/<string:nome>')
class TipoTransacaoNome(Resource):

    @api.marshal_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'nome': 'Nome Tipo Transacao'})
    # @jwt_required
    def get(self, nome):
        """
        Get tipo transacao by Nome
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao_nome(nome)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')
        return tipo_transacao, 200


@api.route('/id/<string:id>')
class TipoContaId(Resource):

    @api.marshal_with(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    # @jwt_required
    def get(self, id):
        """
        Get tipo transacao by ID
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id)
        if not tipo_transacao:
            api.abort(409, 'Tipo Transacao not found')
        return tipo_transacao, 200

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Transacao not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    # @jwt_required
    def delete(self, id):
        """
        Delete tipo transacao by ID
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')

        TipoTransacoes.delete_tipo_transacao(id)
        return {"msg": "Tipo Transacao deleted."}, 200

    @api.expect(tipo_transacao)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        404: 'Tipo Transacao not found',
        422: 'No tipo transacao updated',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Transacao ID'})
    # @jwt_required
    def put(self, id):
        """
        Updates the tipo transacao
        """
        tipo_transacao = TipoTransacoes.get_tipo_transacao(id)
        if not tipo_transacao:
            api.abort(404, 'Tipo Transacao not found')

        TipoTransacoes.update_tipo_transacao(id, api.payload)
        return {"msg": "Tipo Transacao Updated."}, 200

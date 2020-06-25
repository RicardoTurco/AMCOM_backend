from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .serializers import tipo_conta, create_tipo_conta
from .models import TipoContas


api = Namespace('tipo-contas', 'Tipo Contas Endpoint')


@api.route('')
class TipoContaList(Resource):

    @api.marshal_list_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    # @jwt_required
    def get(self):
        """
        Get all tipo contas
        """
        return TipoContas.get_all_tipo_contas(), 200

    @api.expect(create_tipo_conta)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'Tipo Conta already exists',
        422: 'Cannot create tipo conta',
        500: 'Internal Server Error'})
    # @jwt_required
    def post(self):
        """
        Creates a new tipo conta
        """
        tipo_conta_by_name = TipoContas.get_tipo_conta_nome(api.payload.get('tipoconta'))
        if tipo_conta_by_name:
            api.abort(409, 'Tipo Conta already exists')

        TipoContas.insert_tipo_conta(api.payload)
        return {"msg": "Tipo Conta created."}, 201


@api.route('/nome/<string:nome>')
class TipoContaNome(Resource):

    @api.marshal_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'nome': 'Nome Tipo Conta'})
    # @jwt_required
    def get(self, nome):
        """
        Get tipo conta by Nome
        """
        tipo_conta = TipoContas.get_tipo_conta_nome(nome)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')
        return tipo_conta, 200


@api.route('/id/<string:id>')
class TipoContaId(Resource):

    @api.marshal_with(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Pessoa ID'})
    @api.doc(params={'id': 'Tipo Conta ID'})
    # @jwt_required
    def get(self, id):
        """
        Get tipo conta by ID
        """
        tipo_conta = TipoContas.get_tipo_conta(id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')
        return tipo_conta, 200

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Tipo Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Conta ID'})
    # @jwt_required
    def delete(self, id):
        """
        Delete tipo conta by ID
        """
        tipo_conta = TipoContas.get_tipo_conta(id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')

        TipoContas.delete_tipo_conta(id)
        return {"msg": "Tipo Conta deleted."}, 200

    @api.expect(tipo_conta)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        404: 'Tipo Conta not found',
        422: 'No tipo conta updated',
        500: 'Internal Server Error'
    }, params={'id': 'Tipo Conta ID'})
    # @jwt_required
    def put(self, id):
        """
        Updates the tipo conta
        """
        tipo_conta = TipoContas.get_tipo_conta(id)
        if not tipo_conta:
            api.abort(404, 'Tipo Conta not found')

        TipoContas.update_tipo_conta(id, api.payload)
        return {"msg": "Tipo Conta Updated."}, 200

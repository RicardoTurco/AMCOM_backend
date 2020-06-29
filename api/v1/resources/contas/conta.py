from flask_restplus import Resource, Namespace
from .serializers import conta_all, create_conta
from .models import Contas, exist_conta


api = Namespace('contas', 'Contas Endpoint')


@api.route('')
class ContaList(Resource):

    @api.marshal_list_with(conta_all)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all contas
        """
        return Contas.get_all_contas(), 200

    @api.expect(create_conta)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'Conta already exists',
        422: 'Cannot create conta',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new conta
        """
        # Verify if PESSOA has a CONTA of that TIPO ...
        if exist_conta(api.payload.get('idpessoa'), api.payload.get('idtipoconta')):
            api.abort(409, 'Conta already exists')

        Contas.insert_conta(api.payload)
        return {"msg": "Conta created."}, 201


@api.route('/active-accounts')
class ActiveAccounts(Resource):

    @api.marshal_list_with(conta_all)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Contas not found',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all contas active
        """
        contas = Contas.get_contas_flagativo(True)
        if not contas:
            api.abort(404, 'Contas not found')
        return contas, 200


@api.route('/inactive-accounts')
class ActiveAccounts(Resource):

    @api.marshal_list_with(conta_all)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Contas not found',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all contas inactive
        """
        contas = Contas.get_contas_flagativo(False)
        if not contas:
            api.abort(404, 'Contas not found')
        return contas, 200


@api.route('/idpessoa/<string:idpessoa>')
class ContaUsername(Resource):

    @api.marshal_list_with(conta_all)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Conta not found',
        500: 'Internal Server Error'
    }, params={'username': 'Pessoa Username'})
    def get(self, idpessoa):
        """
        Get all contas of Pessoa(idpessoa)
        """
        contas = Contas.get_contas_idpessoa(idpessoa)
        if not contas:
            api.abort(404, 'Conta not found')
        return contas, 200


@api.route('/id/<string:id>')
class ContaId(Resource):

    @api.marshal_with(conta_all)
    @api.doc(reponses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Conta ID'})
    def get(self, id):
        """
        Get conta by ID
        """
        conta = Contas.get_conta(id)
        if not conta:
            api.abort(404, 'Conta not found')
        return conta, 200

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Conta not found',
        500: 'Internal Server Error'
    }, params={'id': 'Pessoa ID'})
    def delete(self, id):
        """
        Delete conta by ID
        """
        conta = Contas.get_conta(id)
        if not conta:
            api.abort(404, 'Conta not found')

        Contas.delete_conta(id)
        return {"msg": "Conta deleted."}, 200


@api.route('/id/<string:id>/inactivate')
class ContaIdInactivate(Resource):

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Conta not found',
        422: 'No inactivate Conta',
        500: 'Internal Server Error'})
    def put(self, id):
        """
        Inactive Conta
        """
        conta = Contas.get_conta(id)
        if not conta:
            api.abort(404, 'Conta not found')

        Contas.update_conta_flagativo(conta['idconta'], False)
        return {"msg": "Conta Inactivated"}, 200


@api.route('/id/<string:id>/activate')
class ContaIdActivate(Resource):

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Conta not found',
        422: 'No activate Conta',
        500: 'Internal Server Error'})
    def put(self, id):
        """
        Active Conta
        """
        conta = Contas.get_conta(id)
        if not conta:
            api.abort(404, 'Conta not found')

        Contas.update_conta_flagativo(conta['idconta'], True)
        return {"msg": "Conta Activated"}, 200

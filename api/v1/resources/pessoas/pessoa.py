from flask_restplus import Resource, Namespace
from .serializers import pessoa, create_pessoa
from .models import Pessoas, exist_pessoa


api = Namespace('pessoas', 'Pessoas Endpoint')


@api.route('')
class PessoaList(Resource):

    @api.marshal_list_with(pessoa)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all pessoas
        """
        return Pessoas.get_all_pessoas(), 200

    @api.expect(create_pessoa)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'Pessoa already exists',
        422: 'Cannot create pessoa',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new pessoa
        """
        # Verify if exists a PESSOA with same "username" and "cpf" ...
        if exist_pessoa(api.payload.get('username'), api.payload.get('cpf')):
            api.abort(409, 'Pessoa already exists')

        Pessoas.insert_pessoa(api.payload)
        return {"msg": "Pessoa created."}, 201


@api.route('/username/<string:username>')
class PessoaUsername(Resource):

    @api.marshal_with(pessoa)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Pessoa not found',
        500: 'Internal Server Error'
    }, params={'username': 'Pessoa Username'})
    def get(self, username):
        """
        Get pessoa by Username
        """
        pessoa = Pessoas.get_pessoa_username(username)
        if not pessoa:
            api.abort(404, 'Pessoa not found')
        return pessoa, 200


@api.route('/cpf/<string:cpf>')
class PessoaCpf(Resource):

    @api.marshal_with(pessoa)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Pessoa not found',
        500: 'Internal Server Error'
    }, params={'username': 'Pessoa Username'})
    @api.doc(params={'cpf': 'Pessoa CPF'})
    def get(self, cpf):
        """
        Get pessoa by CPF
        """
        pessoa = Pessoas.get_pessoa_cpf(cpf)
        if not pessoa:
            api.abort(404, 'Pessoa not found')
        return pessoa, 200


@api.route('/id/<string:id>')
class PessoaId(Resource):

    @api.marshal_with(pessoa)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Pessoa not found',
        500: 'Internal Server Error'
    }, params={'id': 'Pessoa ID'})
    def get(self, id):
        """
        Get pessoa by ID
        """
        pessoa = Pessoas.get_pessoa(id)
        if not pessoa:
            api.abort(404, 'Pessoa not found')
        return pessoa, 200

    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'Pessoa not found',
        500: 'Internal Server Error'
    }, params={'id': 'Pessoa ID'})
    def delete(self, id):
        """
        Delete pessoa by ID
        """
        pessoa = Pessoas.get_pessoa(id)
        if not pessoa:
            api.abort(404, 'Pessoa not found')

        Pessoas.delete_pessoa(id)
        return {"msg": "Pessoa deleted."}, 200

    @api.expect(pessoa)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        404: 'Pessoa not found',
        422: 'No pessoa updated',
        500: 'Internal Server Error'
    }, params={'id': 'Pessoa ID'})
    def put(self, id):
        """
        Updates the user
        """
        pessoa = Pessoas.get_pessoa(id)
        if not pessoa:
            api.abort(404, 'Pessoa not found')

        Pessoas.update_pessoa(id, api.payload)
        return {"msg": "Pessoa Updated."}, 200

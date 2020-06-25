import datetime
from flask_restplus import Resource, Namespace
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_refresh_token_required, get_jwt_identity, get_jwt_claims
from api import jwt
from api.helpers import refresh_parser, check_password
from .serializers import login, full_token, acc_token

from api.v1.resources.pessoas.models import Pessoas


api = Namespace('auth', 'Authentication')


@api.route('/login')
class Login(Resource):

    @api.marshal_with(full_token)
    @api.expect(login)
    @api.doc(responses={
        200: 'Success',
        400: 'Username or password is a required property',
        401: 'Unauthorized',
        404: 'User not found'
    }, security=None)
    def post(self):
        """
        Authentication endpoint
        """
        username = api.payload.get('username')
        password = api.payload.get('password')

        pessoa = Pessoas.get_pessoa_username(username)

        if not pessoa:
            api.abort(404, 'Pessoa not found')

        if not check_password(password, pessoa.get('password')):
            api.abort(401, 'Unauthorized')

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=pessoa, expires_delta=expires)
        refresh_token = create_refresh_token(identity=pessoa)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'name': pessoa.get('username')
        }


@api.route('/refresh')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    @api.expect(refresh_parser)
    @api.doc(responses={
        424: 'Invalid refresh token'
    }, security=None)
    @api.response(200, 'Sucess', acc_token)
    def post(self):
        """
        Retrieve Access Token using Refresh Token
        """
        claims = get_jwt_claims()
        claims['username'] = get_jwt_identity()
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=claims, expires_delta=expires)
        return {'access_token': access_token}


@jwt.user_claims_loader
def add_claims_to_access_token(pessoa):
    return {'privilege': pessoa.get('privilege')}


@jwt.user_identity_loader
def user_identity_lookup(pessoa):
    return pessoa['username']

from flask_restplus import Resource, Namespace


api = Namespace('hello', 'Hello endpoint')


@api.route('/')
class Hello(Resource):

    def get(self):
        """
        Return msg "I'm a a API for AMCOM"
        """
        return {"msg": "I'm a API for AMCOM."}, 200

import uuid
import datetime
from flask import current_app
from api.helpers import encrypt_password


# Conect to 'pessoas' collection in Firebase
def set_pessoas():
    db = current_app.config.get('AMCOM_DB', None)
    pessoas_ref = db.collection('pessoas')
    return pessoas_ref


def date_in(date):
    date_str = date + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def exist_pessoa(username, cpf):
    pessoas_ref = set_pessoas()

    pessoas = [doc.to_dict() for doc in pessoas_ref.where('username', '==', username).where('cpf', '==', cpf).stream()]
    if pessoas:
        return True
    return False


class Pessoas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_pessoas():
        pessoas_ref = set_pessoas()

        all_pessoas = [doc.to_dict() for doc in pessoas_ref.stream()]
        return all_pessoas

    @staticmethod
    def get_pessoa_username(username):
        pessoas_ref = set_pessoas()

        pessoaf = {}
        pessoas = pessoas_ref.where('username', '==', username).stream()
        for pessoa in pessoas:
            pessoaf = pessoa.to_dict()

        if not pessoaf:
            return None
        return pessoaf

    @staticmethod
    def get_pessoa_cpf(cpf):
        pessoas_ref = set_pessoas()

        pessoaf = {}
        pessoas = pessoas_ref.where('cpf', '==', cpf).stream()
        for pessoa in pessoas:
            pessoaf = pessoa.to_dict()

        if not pessoaf:
            return None
        return pessoaf

    @staticmethod
    def get_pessoa(id):
        pessoas_ref = set_pessoas()

        pessoa = pessoas_ref.document(id).get()
        if pessoa.exists:
            return pessoa.to_dict()

        return None

    @staticmethod
    def insert_pessoa(pessoa):
        pessoas_ref = set_pessoas()

        try:
            pessoa['idpessoa'] = str(uuid.uuid4())
            pessoa['password'] = encrypt_password(pessoa.get('password', 'changeme'))
            pessoa['datanascimento'] = date_in(pessoa.get('datanascimento'))

            pessoa_json = {
                "idpessoa": pessoa.get('idpessoa'),
                "nome": pessoa.get('nome'),
                "cpf": pessoa.get('cpf'),
                "datanascimento": pessoa.get('datanascimento'),
                "username": pessoa.get('username'),
                "email": pessoa.get('email'),
                "password": pessoa.get('password')
            }
            pessoas_ref.document(pessoa_json['idpessoa']).set(pessoa_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_pessoa(id, pessoa):
        pessoas_ref = set_pessoas()

        try:
            pessoa['password'] = encrypt_password(pessoa.get('password', 'changeme'))
            pessoa['datanascimento'] = date_in(pessoa.get('datanascimento'))

            pessoa_json = {
                "idpessoa": id,
                "nome": pessoa.get('nome'),
                "cpf": pessoa.get('cpf'),
                "datanascimento": pessoa.get('datanascimento'),
                "username": pessoa.get('username'),
                "email": pessoa.get('email'),
                "password": pessoa.get('password')
            }
            pessoas_ref.document(pessoa_json['idpessoa']).set(pessoa_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_pessoa(id):
        pessoas_ref = set_pessoas()

        pessoas_ref.document(id).delete()

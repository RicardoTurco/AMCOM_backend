import uuid
import datetime
from flask import current_app

from api.v1.resources.pessoas.models import Pessoas
from api.v1.resources.tipo_contas.models import TipoContas


# Conect to 'contas' collection in Firebase
def set_contas():
    db = current_app.config.get('AMCOM_DB', None)
    contas_ref = db.collection('contas')
    return contas_ref


def date_in(date):
    dates = date.strftime("%d/%m/%Y")
    date_str = dates + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def put_fields_missing(conta_dict):

    pessoa = Pessoas.get_pessoa(conta_dict['idpessoa'])
    conta_dict['nome'] = pessoa['nome']
    tipo_conta = TipoContas.get_tipo_conta(conta_dict['idtipoconta'])
    conta_dict['tipoconta'] = tipo_conta['tipoconta']

    return conta_dict


def put_fields_missing_for(all_conta_dict):

    for idx in range(len(all_conta_dict)):
        pessoa = Pessoas.get_pessoa(all_conta_dict[idx]['idpessoa'])
        all_conta_dict[idx]['nome'] = pessoa['nome']
        tipo_conta = TipoContas.get_tipo_conta(all_conta_dict[idx]['idtipoconta'])
        all_conta_dict[idx]['tipoconta'] = tipo_conta['tipoconta']

    return all_conta_dict


def exist_conta(idpessoa, idtipoconta):
    contas_ref = set_contas()

    contas = [doc.to_dict() for doc in contas_ref.where('idpessoa', '==', idpessoa).where('idtipoconta', '==', idtipoconta).stream()]
    if contas:
        return True
    return False


class Contas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_contas():
        contas_ref = set_contas()

        all_contas = [doc.to_dict() for doc in contas_ref.stream()]
        all_contas_f = put_fields_missing_for(all_contas)

        return all_contas_f

    @staticmethod
    def get_contas_flagativo(flagativo):
        contas_ref = set_contas()

        all_contas_flagativo = [doc.to_dict() for doc in contas_ref.where('flagativo', '==', flagativo).stream()]
        all_contas_flagativo_f = put_fields_missing_for(all_contas_flagativo)

        return all_contas_flagativo_f

    @staticmethod
    def get_contas_idpessoa(idpessoa):
        contas_ref = set_contas()

        all_contas_idpessoa = [doc.to_dict() for doc in contas_ref.where('idpessoa', '==', idpessoa).stream()]
        all_contas_idpessoa_f = put_fields_missing_for(all_contas_idpessoa)

        return all_contas_idpessoa_f

    @staticmethod
    def get_conta(id):
        contas_ref = set_contas()

        conta = contas_ref.document(id).get()
        if conta.exists:
            conta_dict = conta.to_dict()
            conta_dict_f = put_fields_missing(conta_dict)
            return conta_dict_f

        return None

    @staticmethod
    def insert_conta(conta):
        contas_ref = set_contas()

        try:
            conta['idconta'] = str(uuid.uuid4())
            conta['datacriacao'] = date_in(datetime.datetime.now())

            conta_json = {
                "idconta": conta.get('idconta'),
                "idpessoa": conta.get('idpessoa'),
                "saldo": 0.00,
                "limitesaquediario": conta.get('limitesaquediario'),
                "idtipoconta": conta.get('idtipoconta'),
                "flagativo": True,
                "datacriacao": conta.get('datacriacao')
            }
            contas_ref.document(conta_json['idconta']).set(conta_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_conta_flagativo(id, flagativo):
        contas_ref = set_contas()

        try:
            conta_flagativo = {
                "flagativo": flagativo
            }
            contas_ref.document(id).set(conta_flagativo, merge=True)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_conta(id):
        contas_ref = set_contas()

        contas_ref.document(id).delete()

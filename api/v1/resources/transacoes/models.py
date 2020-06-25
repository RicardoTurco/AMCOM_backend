import uuid
import datetime
from flask import current_app

from api.v1.resources.contas.models import set_contas, Contas
from api.v1.resources.tipo_transacoes.models import TipoTransacoes


# Conect to 'transacoes' collection in Firebase
def set_transacoes():
    db = current_app.config.get('AMCOM_DB', None)
    transacoes_ref = db.collection('transacoes')
    return transacoes_ref


def date_in(date):
    dates = date.strftime("%d/%m/%Y")
    date_str = dates + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    return date_f


def put_fields_missing(transacao_dict):

    tipo_transacao = TipoTransacoes.get_tipo_transacao(transacao_dict['idtipotransacao'])
    transacao_dict['tipotransacao'] = tipo_transacao['tipotransacao']
    transacao_dict['operacao'] = tipo_transacao['operacao']

    return transacao_dict


def put_fields_missing_for(all_transacoes_dict):

    for idx in range(len(all_transacoes_dict)):
        tipo_transacao = TipoTransacoes.get_tipo_transacao(all_transacoes_dict[idx]['idtipotransacao'])
        all_transacoes_dict[idx]['tipotransacao'] = tipo_transacao['tipotransacao']
        all_transacoes_dict[idx]['operacao'] = tipo_transacao['operacao']

    return all_transacoes_dict


def update_saldo_conta(idconta, idtipotransacao, valor, origin):
    """
    Param 'origin':

    Only can be ("I" or "D"). Defines how the 'saldo' of 'conta' will be adjusted.
    Any other option, the 'saldo' remain the same.
    """
    conta = Contas.get_conta(idconta)
    if conta:

        tipo_transacao = TipoTransacoes.get_tipo_transacao(idtipotransacao)
        if tipo_transacao:

            new_saldo = conta['saldo']
            if origin == 'I':
                if tipo_transacao['operacao'] == 'D':
                    new_saldo = conta['saldo'] - valor
                elif tipo_transacao['operacao'] == 'C':
                    new_saldo = conta['saldo'] + valor
            elif origin == 'D':
                if tipo_transacao['operacao'] == 'D':
                    new_saldo = conta['saldo'] + valor
                elif tipo_transacao['operacao'] == 'C':
                    new_saldo = conta['saldo'] - valor

            conta_new_saldo = {
                "saldo": new_saldo
            }
            contas_ref = set_contas()
            contas_ref.document(conta['idconta']).set(conta_new_saldo, merge=True)


class Transacoes:

    def __init__(self):
        pass

    @staticmethod
    def get_all_transacoes():
        transacoes_ref = set_transacoes()

        all_transacoes = [doc.to_dict() for doc in transacoes_ref.stream()]
        all_transacoes_f = put_fields_missing_for(all_transacoes)

        return all_transacoes_f

    @staticmethod
    def get_all_transacoes_conta(idconta):
        transacoes_ref = set_transacoes()

        all_transacoes_conta = [doc.to_dict() for doc in transacoes_ref.where('idconta', '==', idconta).stream()]
        all_transacoes_conta_f = put_fields_missing_for(all_transacoes_conta)

        return all_transacoes_conta_f

    @staticmethod
    def get_transacao(id):
        transacoes_ref = set_transacoes()

        transacao = transacoes_ref.document(id).get()
        if transacao.exists:
            transacao_dict = transacao.to_dict()
            transacao_dict_f = put_fields_missing(transacao_dict)
            return transacao_dict_f

        return None

    @staticmethod
    def insert_transacao(transacao):
        transacoes_ref = set_transacoes()

        try:

            transacao['idtransacao'] = str(uuid.uuid4())
            transacao['datatransacao'] = date_in(datetime.datetime.now())

            transacao_json = {
                "idtransacao": transacao.get('idtransacao'),
                "idconta": transacao.get('idconta'),
                "idtipotransacao": transacao.get('idtipotransacao'),
                "valor": transacao.get('valor'),
                "datatransacao": transacao.get('datatransacao')
            }
            transacoes_ref.document(transacao_json['idtransacao']).set(transacao_json)

            update_saldo_conta(transacao_json['idconta'],
                               transacao_json['idtipotransacao'],
                               transacao_json['valor'],
                               'I')

        except Exception as e:
            return f"An Error Occured: {e}"

    @staticmethod
    def delete_transacao(transacao):
        transacoes_ref = set_transacoes()

        transacoes_ref.document(transacao['idtransacao']).delete()

        update_saldo_conta(transacao['idconta'],
                           transacao['idtipotransacao'],
                           transacao['valor'],
                           'D')

import uuid
from flask import current_app


# Conect to 'tipo_transacoes' collection in Firebase
def set_tipo_transacoes():
    db = current_app.config.get('AMCOM_DB', None)
    tipo_transacoes_ref = db.collection('tipo_transacoes')
    return tipo_transacoes_ref


class TipoTransacoes:

    def __init__(self):
        pass

    @staticmethod
    def get_all_tipo_transacoes():
        tipo_transacoes_ref = set_tipo_transacoes()

        all_tipo_transacoes = [doc.to_dict() for doc in tipo_transacoes_ref.stream()]
        return all_tipo_transacoes

    @staticmethod
    def get_tipo_transacao_operacao(operacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        tipo_transacoes = [doc.to_dict() for doc in tipo_transacoes_ref.where('operacao', '==', operacao).stream()]
        return tipo_transacoes

    @staticmethod
    def get_tipo_transacao_nome(nome_tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        tipo_transacaof = {}
        tipo_transacoes = tipo_transacoes_ref.where('tipotransacao', '==', nome_tipo_transacao).stream()
        for tipo_transacao in tipo_transacoes:
            tipo_transacaof = tipo_transacao.to_dict()

        if not tipo_transacaof:
            return None
        return tipo_transacaof

    @staticmethod
    def get_tipo_transacao(id):
        tipo_transacoes_ref = set_tipo_transacoes()

        tipo_transacao = tipo_transacoes_ref.document(id).get()
        if tipo_transacao.exists:
            return tipo_transacao.to_dict()

        return None

    @staticmethod
    def insert_tipo_transacao(tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        try:
            tipo_transacao['idtipotransacao'] = str(uuid.uuid4())

            tipo_transacao_json = {
                "idtipotransacao": tipo_transacao.get('idtipotransacao'),
                "tipotransacao": tipo_transacao.get('tipotransacao'),
                "operacao": tipo_transacao.get('operacao')
            }
            tipo_transacoes_ref.document(tipo_transacao_json['idtipotransacao']).set(tipo_transacao_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_tipo_transacao(id, tipo_transacao):
        tipo_transacoes_ref = set_tipo_transacoes()

        try:
            tipo_transacao_json = {
                "idtipotransacao": id,
                "tipotransacao": tipo_transacao.get('tipotransacao'),
                "operacao": tipo_transacao.get('operacao')
            }
            tipo_transacoes_ref.document(tipo_transacao_json['idtipotransacao']).set(tipo_transacao_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_tipo_transacao(id):
        tipo_transacoes_ref = set_tipo_transacoes()

        tipo_transacoes_ref.document(id).delete()

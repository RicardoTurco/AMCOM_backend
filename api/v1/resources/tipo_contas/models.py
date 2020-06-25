import uuid
from flask import current_app


# Conect to 'tipo_contas' collection in Firebase
def set_tipo_contas():
    db = current_app.config.get('AMCOM_DB', None)
    tipo_contas_ref = db.collection('tipo_contas')
    return tipo_contas_ref


class TipoContas:

    def __init__(self):
        pass

    @staticmethod
    def get_all_tipo_contas():
        tipo_contas_ref = set_tipo_contas()

        all_tipo_contas = [doc.to_dict() for doc in tipo_contas_ref.stream()]
        return all_tipo_contas

    @staticmethod
    def get_tipo_conta_nome(nome_tipo_conta):
        tipo_contas_ref = set_tipo_contas()

        tipo_contaf = {}
        tipo_contas = tipo_contas_ref.where('tipoconta', '==', nome_tipo_conta).stream()
        for tipo_conta in tipo_contas:
            tipo_contaf = tipo_conta.to_dict()

        if not tipo_contaf:
            return None
        return tipo_contaf

    @staticmethod
    def get_tipo_conta(id):
        tipo_contas_ref = set_tipo_contas()

        tipo_conta = tipo_contas_ref.document(id).get()
        if tipo_conta.exists:
            return tipo_conta.to_dict()

        return None

    @staticmethod
    def insert_tipo_conta(tipo_conta):
        tipo_contas_ref = set_tipo_contas()

        try:
            tipo_conta['idtipoconta'] = str(uuid.uuid4())

            tipo_conta_json = {
                "idtipoconta": tipo_conta.get('idtipoconta'),
                "tipoconta": tipo_conta.get('tipoconta')
            }
            tipo_contas_ref.document(tipo_conta_json['idtipoconta']).set(tipo_conta_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_tipo_conta(id, tipo_conta):
        tipo_contas_ref = set_tipo_contas()

        try:
            tipo_conta_json = {
                "idtipoconta": id,
                "tipoconta": tipo_conta.get('tipoconta')
            }
            tipo_contas_ref.document(tipo_conta_json['idtipoconta']).set(tipo_conta_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_tipo_conta(id):
        tipo_contas_ref = set_tipo_contas()

        tipo_contas_ref.document(id).delete()

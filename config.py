import sys
from firebase_admin import credentials, firestore, initialize_app


class BaseConfig:

    DEBUG = True
    RESTPLUS_VALIDATE = True
    ERROR_INCLUDE_MESSAGE = False
    RESTPLUS_MASK_SWAGGER = False
    JWT_SECRET_KEY = 'SECRET_KEY'

    try:
        # Conecting Firebase DB
        AMCOM_KEY = credentials.Certificate('keys.json')
        AMCOM_APP = initialize_app(AMCOM_KEY)
        AMCOM_DB = firestore.client()
    except Exception as e:
        print(e)
        sys.exit()


class ProdConfig(BaseConfig):

    DEBUG = False


class DevConfig(BaseConfig):

    pass

# [DOCK] Selection challenge
This project is the "challenge" for a developer position in the company [Dock].  
(The instructions for this challenge are in readme_dock.md file)

## Deploy

The API was deployed on Heroku:

```
URL of Swagger on Heroku: 
https://dockapi.herokuapp.com/api/v1/docs
```

## BD - Firebase

For data storage, the Firebase database is used.  
The connection keys are in the KEYS.JSON file.

![Alt text](imgs/entidades.png?raw=true)

## Installing

To install and execution the API in your local machine, you will need to:

```
git clone https://github.com/RicardoTurco/desafio-dev-api-rest.git && cd desafio-dev-api-rest

Create and activate one "virtualenv"
(using any valid form) 

pip install -r requirements.txt

python run.py
```

## Swagger

After the application goes up, open your browser on `localhost:5000/api/v1/docs` to see the self-documented interactive API.

## Basic WorkFlow

```   
- Import Test_Dock.postman_collection.json in Postman to access the URLs and payloads;
- A User's "access_token" must be informed in the HEADER of requests;
- When "access_token" expires, you must use the "refresh_token" in HEADER of URL 
(POST > localhost:5000/api/v1/auth/refresh) to update a user's "access_token";


a) Login using the username "admin" and password "senhaadmin" to get ACCESS_TOKEN;
(This is the only URL that is not required to provide an "access_token")
(POST > localhost:5000/api/v1/auth/login)

b) Criar um USER usando o "access_token" do ADMIN;
(POST > http://127.0.0.1:5000/api/v1/pessoas)

c) Realizar o LOGIN utilizando o "username" e o "password" o USER criado, para acessar o ACCESS_TOKEN
(POST > http://127.0.0.1:5000/api/v1/auth/login)

d) List ALL Pessoas;
(GET > http://127.0.0.1:5000/api/v1/pessoas)

e) List ALL tipos de Contas;
(GET > http://127.0.0.1:5000/api/v1/tipo-contas)

f) Create CONTA to Pessoa;
(POST > http://127.0.0.1:5000/api/v1/contas)

g) List ALL Contas;
(GET > http://127.0.0.1:5000/api/v1/contas)

h) List ALL tipo de Transacoes;
(GET > http://127.0.0.1:5000/api/v1/tipo-transacoes)

i) Create TRANSACAO;
(POST > http://127.0.0.1:5000/api/v1/transacoes)
```



## Project Structure

The project structure is based on the official [Scaling your project](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-apis-with-reusable-namespaces) doc with some adaptations (e.g `v1` folder to agroup versioned resources).

```
.
├── api
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── parsers.py
│   │   └── password.py
│   └── v1
│   │   ├── __init__.py
│   │   └── resources
│   │       ├── auth
│   │       │   ├── __init__.py
│   │       │   ├── login.py
│   │       │   └── serializers.py
│   │       └── contas
│   │       │   ├── __init__.py
│   │       │   ├── conta.py
│   │       │   ├── models.py
│   │       │   └── serializers.py
│   │       ├── hello
│   │       │   ├── __init__.py
│   │       │   ├── hello.py
│   │       └── pessoas
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── pessoa.py
│   │       │   └── serializers.py
│   │       └── tipo_contas
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── serializers.py
│   │       │   └── tipo_conta.py
│   │       └── tipo_transacoes
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── serializers.py
│   │       │   └── tipo_transacao.py
│   │       └── transacoes
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── serializers.py
│   │       │   └── transacao.py
│   │       ├── __init__.py
│   ├── __init__.py
├── imgs
│   ├── images files
├── .gitignore
├── config.py
├── keys.json
├── Procfile
├── README.md
├── readme_dock.md
├── requirements.txt
├── run.py
├── runtime.txt
├── Test_Dock.postman_collection.json

```

### Folders

* `api` - All the RESTful API implementation is here.
* `api/helpers` - Useful function/class helpers for all modules.
* `api/v1` - Resource agroupment for all `v1` [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces).
* `api/v1/resources` - All `v1` resources are implemented here.
* `imgs` - All images files of API project/documentation.

### Files

* `api/__init__.py` - The Flask Application factory (`create_app()`) and it's configuration are done here. Your [Blueprints](https://flask-restplus.readthedocs.io/en/stable/scaling.html#use-with-blueprints) are registered here.
* `api/v1/__init__.py` - The Flask RESTPlus API is created here with the versioned Blueprint (e.g `v1`). Your [Namespaces](https://flask-restplus.readthedocs.io/en/stable/scaling.html#multiple-namespaces) are registered here.
* `.gitignore` - Lists files and directories which should not be added to git repository.
* `config.py` - Config file for envs, global config vars and so on.
* `keys.json` - Keys for access for Firebase DB.
* `Procfile` - Configuration of gunicorn (for deploy on Heroku).
* `README.md` - Instructions and informations of this "challenge".
* `readme_dock.md` - Instructions how to execute of this "challenge.
* `requirements.txt` - All project dependencies.
* `run.py` - The Application entrypoint.
* `runtime.py` - Set version of Python for deploy on Heroku.
* `Test_Dock.postman_collection.json` - File to import in Postman.

### API Versioning

If you need to create another API version (like `/api/v2`), follow these steps:

First, create your `v2` API structure folder:

```
mkdir api/v2
touch api/v2/__init__.py
```

Inside your `api/v2/__init__.py` create your Blueprint:

```
from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')
```

Create your resources and namespaces inside `api/v2/resources` (like the `api/v1/resources`) and register them:

```
# api/v2/__init__.py

from flask import Blueprint
from flask_restplus import Api

v2_blueprint = Blueprint('v2', __name__, url_prefix='/api/v2')

api = Api(v2_blueprint,
          doc='/docs',
          title='Flask App',
          version='2.0',
          description='Flask RESTful API V2')


# Fictious resource example
from .resources.auth.login import api as auth_ns
api.add_namespace(auth_ns)

```

And finally, register your Blueprint with the Flask Application:

```
# api/__init__.py

# config code...
from api.v1 import v1_blueprint
    api.register_blueprint(v1_blueprint)

from api.v2 import v2_blueprint
    api.register_blueprint(v2_blueprint)

```

Now you have your new endpoints with the base path `/api/v2` :) !

OBS: Your swagger docs for this new API version will be under this base path too. Ex: `localhost:5000/api/v2/docs`.

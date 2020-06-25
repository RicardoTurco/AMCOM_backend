from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    jwt.init_app(app)

    from api.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint)

    CORS(app)
    return app

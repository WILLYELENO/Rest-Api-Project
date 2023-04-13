import os
import secrets #para encriptar codigo de la clave secreta de jwt
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate



from db import db
from blocklist import BLOCKLIST
import models
# BLueprint:
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url= None):
#   Es mejor guardar todo este fragmento de congiguracion dentro de una funcion
#cuya finalidad sea crear y configurar.
#Es mejor a la hora de realizar pruebas.
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app) #Conecta la aplicacion de FLASK a SQLalchemy
    #Instancia de migracion (SIempre va despues de db.init_app(app))
    migrate = Migrate(app, db)
    api = Api(app)


#   CONFIGURACION DE JWT:
    #CLAVE SECRETA JWT:
    app.config["JWT_SECRET_KEY"] = "320120231160252190274514617873679966463" 
    #importamos el modulo secrets en la app
    # Igualamos ["JWT_SECRET_KEY"]  a esto: secrets.SystemRandom().getrandbits(128). esto ultimo es el largo de la clave
    # abrimos la terminal y ejecutamos "python3", luego secrets y luego copiamos y pegamos secrets.SystemRandom().getrandbits(128)
    #Luego de ejecutar todo eso, me genera el token y lo reemplazo como clave secreta
    # Instancia de JWT:
    jwt = JWTManager(app) 


#   ESTOS DOS DECORADORES, LOS USO JUNTO CON EL ARCHIVO BLOCKLIST para almacenar los token ya utilizados.

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "El token ha caducado.", "error": "token_expired"}),
            401,
        )


    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
    
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "El token ha caducado.", "error": "token_expire"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # JWT configuration ends
#   Aca le indico que con la primera peticion que se haga, antes de inicializar
# mi app de flask, primero que cree todas las tablas en la db, si es que no existen ya
#    sql sabe que tablas crear porque arriba importamos los models
    @app.before_first_request
    def create_tables():
        
        db.create_all()
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

app = create_app()

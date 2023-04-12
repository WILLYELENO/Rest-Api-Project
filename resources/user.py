from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

#   create_access_token: COmbinacion de numeros y caracteres que vamos a generar en el servidor,
#lo enviamos al cliente y la unica manera de obtenerlo es proporcionandonos el nombre de usuario
# y la contraseña correctos. Una vez que suceda eso, le enviamos al cliente y este lo almacenara y en
#cada peticion nos lo devolverá.

#Vamos a utilizar para hashear la contraseña que envía el cliente.
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Un usuario con ese nombre ya existe.")
#   Si no existe el usuario, lo creamos con nuestro modelo de usuario.
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
#   comprobamos si el usuario existe.
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):#(contraseña que viene de la db):
#   Si la contraseña del usuario coincide con la que estya en la db, entonces diremos que el
#token de acceso es igual a la funcion 'create_access_token' que viene del módulo que importamos arriba
# el parámetro 'identity = es la entidad o valor que se guarda en el token (el id del registro de ese usuario)
# el parámetro 'fresh' = es que se va a actualiza.
#vienen otros parametros como timedelta que fija limite de tiempo por ejemplo.
            access_token = create_access_token(identity=user.id, fresh=True)

            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token }, 200
#   Cuando se loguee, la respuesta de la peticion enviara dos token: el de acceso y el de refresh
#El de refresh será utilizado en este ejemplo, en el endpoint de refresh únicamente.
#Ese endpoint devolverá un token de refresco que hara la funcion del token de acceso.
#Básicamente lo usa para renovar el roken de acceso, es decir para renovarlo, debe dirigirse al endpoint
#de refresh, carga el token de refresh del endpoint de login y ahi le devolverá un nuevo token de acceso
#A su vez, el token viejo de acceso se guardará en la lista del archivo BLOCKLIST

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    Este recurso puede ser útil al probar nuestra aplicación Flask.
    Puede que no queramos exponerlo a los usuarios públicos, pero por el
    En aras de la demostración en este curso, puede ser útil
    cuando estemos manipulando datos de los usuarios.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) # Al colocar como parametro el refresh, le estamos indicando que solo requiere el refresh token
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Deje en claro que cuándo agregar el token de actualización a la lista de bloqueo dependerá del diseño de la aplicación
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) #AGrego a la lista de bloqueos el token refresh tambien
        return {"access_token": new_token}, 200
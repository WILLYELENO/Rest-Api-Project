import uuid
#from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
#from db import stores


from db import db
from models.store import StoreModel
from schemas import StoreSchema

#Creacion y definicion de bluprint. Hay que importarlo desde el archivo app.py
blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<int:store_id>")
#Este decorador flask_smorest con esta vista del método de flask
#para que cuando hagamos una peticion a este endpoint, se ejecute 
#cualquiera de los métodos definidos dentro de la clase(segun sea
# get, post, put, delete, etc)
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        
        

#   Los delete de todas las clases no fueron decorados porque
#   no es necesario ya que solo devuelven un mensaje...
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Tienda eliminada"}
        #raise NotImplementedError("Deleting a store is not implemented.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self, store_data):
        #store_data = request.get_json()
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
#   Se prevé este error, por en el modelo Store, se previó que el name era unico
            abort(400, message ="ya sale una tienda con ese nombre")
        except SQLAlchemyError:
            abort(500, message ="Se ha producido un error al insertar la tienda")

        return store
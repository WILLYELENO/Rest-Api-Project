
#from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy.exc import SQLAlchemyError

#from db import items
from db import db
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    @jwt_required()
    def get(self, item_id):
#   En lugar de encontrar los datos en la lista de articulos, vamos a ir a la db y lño que hay que hacer
# es borrar el codigo comentato y colocar lo siguiente...   
#el articulo o item es igual al item.model y el atributo query que viene del modelo de la db.Model
        item = ItemModel.query.get_or_404(item_id)
#    get_or_404(item_id): hace que el item cargado en la base de dato 
# sea recuperado utilizando el id del item del request (que viene de insonmia)
#en el caso de que no lo consiga, aborta todo automaticamente...por eso no es necesario la gestion de errores 
#por nosotros...
        """try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")"""
        return item
    

#Del mismo modo que en la funcion de arriba,vamos a agarrar elk modelo del elemento o item
#para que podamos desacernos de este error, excepto
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is admin"):
            abort(401, message="Se requieren permisos de administrador")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item eliminado"}

    @blp.arguments(ItemUpdateSchema)
#Al colocar este decorador, lo que hace por atras es que se activa
# la clase ItemSchema y procede a validar los datos que envia el usuario(en el json)
# y si son correctos, hace que el método que se encuentre debajo de este decorador
# le otorgue como argumento, un diccionario validado para que podamos trabajar
#con los datos contenidos en el. Ese diccionario esta representado por "item_data" 
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):
    # el item_data es lo que retorna el esquema de validacion ItemSchema
    # este argumento es utilizado por la funcion y siempŕe se coloca delante
    # del argumento raiz    
       # ¡Hay más validación que hacer aquí!
        # Como asegurarse de que el precio sea un número y que ambos elementos sean opcionales
        # Difícil de hacer con una sentencia if...
        """
        try:
            item = items[item_id]
            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")"""
        
        item = ItemModel.query.get_or_404(item_id)
        if Item: #si el item existe...
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:# si no existe, se deberá pasar el precio, nombre y el id de la tienda, ya que estoy usando el model completo con los **
            item= ItemModel(id= item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

        #raise NotImplementedError("La actualizacion de un item no esta implementado")
        


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many = True)) #many convierte toda ersa consulta en una lista
    def get(self):
        return ItemModel.query.all()
    


    #@jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
#Al colocar este decorador, es la respuesta que voy a enviar...
    def post(self, item_data): 
        # Luego, retorna un item_data en formato json que recibe el método post
        # como argumento para poder trabajarlo.
        # Entonces esta linea no hace falta: item_data = request.get_json()
        """
        no sirve mas esta comprobacion.
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")"""

        """Y COMO AHORA VAMOS A TRABAJAR CON objetos del modelo
        de items en lugar de diccionarios, esto tampoco lo necesitamos:
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item"""
#   Entonces, creamos el modelo de items al que le pasaremos los datos
#que recibimos en el método post (a través de insonmia) con los **
#LO que hace es convertir el diccionario en argumentos de clave
#( alli estaran los parametros de la tabla model)
        item = ItemModel(**item_data) #Recibo lo de insonmia
        try:
            db.session.add(item) #Agrego lo de insonmia
            db.session.commit()#huardo lo de insonmia
        except SQLAlchemyError:
            abort(500, message ="Se ha producido un error al insertar el articulo")

        return item

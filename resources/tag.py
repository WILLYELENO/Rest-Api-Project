
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

#from db import items
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operaciones con Tags")



#Recuperacion de etiquetas:
@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
#Recuperación de las etiquetas;    
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
#Creacion de etiquetas;
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    #tag_data es el resultado de la validacion del schema
    #store_id lo obtenemos de la url, por eso es que lo igualamos
    def post(self,tag_data, store_id):
#   Para comprobar el nombre +el id haríamos esto...
        #if TagModel.query.filter(TagModel.store_id== store_id, TagModel.name == tag_data["name"]).first():
            #abort(400, message = "Ya existe una etiqueta de mensaje con ese nombre en este almacen")
            tag = TagModel(**tag_data, store_id = store_id)

            try:
                db.session.add(tag)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(500, message= str(e))
            
            return tag


#Actualizacion de etiquetas
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
#Desvincular un elemento de una etiqueta o viceversa:    
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}





#Recuperar etiqueta en particular:

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag= TagModel.query.get_or_404(tag_id)
#    get_or_404(item_id): hace que el tag cargado en la base de datos 
# sea recuperado utilizando el id del tag del request (que viene de insonmia)
#en el caso de que no lo consiga, aborta todo automaticamente...por eso no es necesario la gestion de errores 
#por nosotros...
        return tag
    @blp.response(
        202,
        description="Elimina una etiqueta si no hay ningún elemento etiquetado con ella.",
        example={"message": "Etiqueta eliminada"},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Devuelto si la etiqueta se asigna a uno o más elementos. En este caso, la etiqueta no se elimina.",
    )
#   Eliminar una etiqueta
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="No se pudo eliminar la etiqueta. Asegúrese de que la etiqueta no esté asociada con ningún elemento y vuelva a intentarlo.",  # noqa: E501
        )

    
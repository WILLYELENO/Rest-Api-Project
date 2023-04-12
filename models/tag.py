from db import db


class TagModel(db.Model):
    #nombre de la tabla:
    __tablename__ = "tags"
    #Columnas:
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    store_id = db.Column(db.String(), db.ForeignKey("stores.id"), nullable=False)

    store =db.relationship("StoreModel", back_populates = "tags") 
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
    #con secondary hacemos referencia a la tabla item_tags, asi sqlalchemy sabra que tiene
    #que ir a través de la tabla secundaria pára encontrar con que articulos o items
    #esta relacionada esta etiqueta. Asi, mirara las id de la tag que esta vinculada con
    # el id de la etiqueta y nos dará los articulos que estan relacionados.
    
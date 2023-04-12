from db import db


class ItemModel(db.Model):
    #nombre de la tabla:
    __tablename__ = "items"
    #Columnas:
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String)
    #unique = unico / nullable = no se puede crear un elemento que no tenga nombre
    price = db.Column(db.Float(precision=2), unique= False, nullable=False)
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"), unique=False, nullable=False)
    #   db.ForeignKey("stores.id") este es el agregado para relacionar este campo con el campo de la otra tabla
    #lo que hace es guardar ese id de la tabla stores en el campo "store_id" de esta tabla
    store = db.relationship("StoreModel", back_populates= "items")
    #   con el relationship guardo el obvjeto de la tabla store aqui en esta variable
    #    el populates se utiliza para que esta tabla tenga una "mencion" o relacion
    #en la tabla stores. Va a tener un objeto anidado..
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")




from db import db


class StoreModel(db.Model):
    #nombre de la tabla:
    __tablename__ = "stores"
    #Columnas:
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    #unique = unico / nullable = no se puede crear un elemento que no tenga nombre
    items = db.relationship("ItemModel", back_populates = "store", lazy = "dynamic", cascade= "all,delete") 
    #   lazy=dinamic significa que los items aquí no van a ser recuperado de la db hasta que se lo digamos
    # tendra una lista anidada de objetos del modelo artículo.
    #cascade= "all,delete" = logramos que cuando se borre la tienda, se borren tambien los items que poseia
    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic", cascade= "all,delete") 
    
    
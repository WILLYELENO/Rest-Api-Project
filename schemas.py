from marshmallow import Schema, fields

#Requisitos de datos para cada endpoint:

#Con estos comprobalos los datos que nos envía el cliente...

#Nuestros esquemas tienen que reflejar que el modelo item tendra un objeto
#anidado y que el modelo store tendra una lista de objetos tienda anidados.
#POr ello vamos a distinguir entre esquemas simples y especiales.



#Esquemas de articulos simple
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) #dump_only significa que es solo para devolver datos desde la API, no lo generamos nosotros 
    name = fields.Str(required=True)#Required: si o si deben estar dentro de la peticion del cliente
    price = fields.Float(required=True)
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()



class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True) 
#load_only = evita que nosotros le enviemos la contraseña al cliente.

#Esquemas que contemplan relaciones entre tablas:

class ItemUpdateSchema(Schema):
    #COmo ambos campos no tienen nada, pueden no enviarse ambos o solo uno.
    name = fields.Str()
    price = fields.Float()
    store_id = fields. Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only= True)
    tags = fields.Nested(PlainTagSchema(), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only= True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)



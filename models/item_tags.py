from db import db



#Modelo secundario que describe la vinculacion entre la tabla items y la de tags
class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)

    #campo que enlasa con los items
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    
    #campo que enlasa con los tags
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
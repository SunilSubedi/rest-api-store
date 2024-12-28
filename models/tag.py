from db import db

class TagModel(db.Model): #Inhertis a Model form db which is sqlachamy
    #define table name
    __tablename__ = "tags"
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False, unique=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),nullable=False,unique=False)
    
    store = db.relationship("StoreModel",back_populates="tags",lazy="select")
    
    items = db.relationship("ItemModel", back_populates="tags",secondary="items_tags")
    
    
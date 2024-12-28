import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from schemas import StoreSchema,StoreUpdateSchema

blb = Blueprint("stores",__name__,description="Operations on store")

@blb.route("/store/<int:store_id>")
class Store(MethodView): #Operation here is for one store id at a time
    @blb.response(200,StoreSchema)
    def get(self,store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store
   
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        
        return {"status":"deleted"} , 201
    
       
    
    @blb.arguments(StoreUpdateSchema)
    @blb.response(200,StoreSchema)
    def put(self,new_data,store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Updating Store not implemented")
    
    
@blb.route("/store")
class Stores(MethodView): #Operation here is create and views all the store
    @blb.response(201,StoreSchema(many=True))
    def get(self):
        store = StoreModel.query.all()
        return store
    
    @blb.arguments(StoreSchema)
    @blb.response(201,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="The store name already exits")
        except SQLAlchemyError:
            abort(500,message="Error Adding data")        
            
        return store, 201
    
    
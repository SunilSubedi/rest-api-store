
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required,get_jwt, create_refresh_token, get_jwt_identity

from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("users",__name__,description="User Operation here.")

@blp.route("/user/<int:user_id>")
class UserUpdate(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def put(self,user_data,user_id):
        pass
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
          db.session.delete(user)
          db.session.commit()
        except SQLAlchemyError:
            abort(404, description="Cannot find user.")  
        return {"message":"user deleted "},200
    
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=str(user.id))
            refesh_token = create_refresh_token(identity=str(user.id))
            
            return{"access_token":access_token,"refesh_token":refesh_token}
        
        abort(404, message="Invalids Credentials")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()        
        new_token = create_access_token(identity=current_user, fresh=False)
               
    

@blp.route("/register")
class User(MethodView):
    def get(self):
        pass
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exits")
        user = UserModel(
            username=user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(404,description="Cannot add user")   
        
        return {"message":"User Created Successfully"},201
    
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return{"message":"Successfully logged out"}
         
            
            
        
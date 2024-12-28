from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import models
from db import db
from flask_migrate import Migrate
from resources.item import blp as ItemBluePrint
from resources.store import blb as StoreBluePrint
from resources.tag import blp as  TagBluePrint
from resources.user import blp as UserBluePrint
import os
from blocklist import BLOCKLIST

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"]= "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]= db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    
    db.init_app(app)
     
    
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"]= "104331001391196150175590849077659877240"
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({
                "description":"The token has been revoked.",
                "error":"token_revoked"
            })
        )
    
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return(
            jsonify({
                "description":"The token is not fresh",
                "error":"fresh_token_required"
            })
        )
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({
                "message":"The token has expired",
                "error": "token_expired"
            })
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({
                "message":"Signature verification failed", 
                "error":"Invalid_token"
            })
        ) 
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify({
                "description":"Request does not contain an access token",
                "error":"authorization_required"
            })
        )
           
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)
    
    migrate = Migrate(app,db)
    
    return app

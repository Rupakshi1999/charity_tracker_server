from flask import Flask
from flask_restx import Api
from models import Recipe, User, Donation, Charities
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipies import recipie_namespace
from auth import auth_namespace
from donations import donation_namespace
from charities import charity_namespace
from flask_cors import CORS
from config import DevConfig

def create_app():
    config=DevConfig
    # config the app
    app=Flask(__name__)
    app.config.from_object(config)

    # Config api to work with an application that's located on a different port 
    # (backend is running on 5000 frontend is running on 3000)
    CORS(app)


    # register sqlalchemy to work with our app
    db.init_app(app)

    # add to database file without hacing to recreate it in cmd `echo $FLASK_APP`
    migrate=Migrate(app, db)

    # login 
    JWTManager(app)

    api=Api(app,doc='/docs')
    api.add_namespace(recipie_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(donation_namespace)
    api.add_namespace(charity_namespace)
        

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "recipe":Recipe,
            "user":User,
            "donations":Donation,
            "charities":Charities
        }

    return app

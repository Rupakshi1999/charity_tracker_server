from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

# config the app
app=Flask(__name__)
app.config.from_object(DevConfig)

# register sqlalchemy to work with our app
db.init_app(app)

# add to database file without hacing to recreate it in cmd `echo $FLASK_APP`
migrate=Migrate(app, db)

# login 
JWTManager(app)

api=Api(app,doc='/docs')

# Searilize the database data into json to use on front end
recipe_model=api.model(
    # model {searializer tem[plate]}
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)

signup_model=api.model(
    # model {searializer tem[plate]}
    "signup",
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model=api.model(
    # model name {searializer tem[plate]}
    "login",
    {
        "username":fields.String(),
        "password":fields.String()
    }
)

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}
    
@api.route('/signup')
class SignUp(Resource):

    # show the format of data in /docs post
    @api.expect(signup_model)
    def post(self):
        signup_data = request.get_json()

        username=signup_data.get('username')
        db_user=User.query.filter_by(username=username).first()

        if db_user is not None:
            return jsonify({"message":f"User with username {username} already exists"})
        
        email= signup_data.get('email')
        db_email=User.query.filter_by(email=email).first()

        if db_email is not None:
            return jsonify({"message":f"Email {email} already exists"})


        new_user = User(
            username = signup_data.get('username'),
            email = signup_data.get('email'),
            password = generate_password_hash(signup_data.get('password'))
        )

        new_user.save()

        return jsonify({"message":f"User {username} created successfully"})

@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        login_data=request.get_json()

        username = login_data.get('username')
        password = login_data.get('password')

        db_user= User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
        
        return jsonify({"access token":access_token, "refresh token":refresh_token})



@api.route('/recipes')
class RecipesResource(Resource):

    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from the databse"""
        # Get the recipes in sqlalchemy object
        recipes = Recipe.query.all()

        # convert it into json using serilizer and return
        return recipes

    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    @jwt_required()
    def post(self):
        """Create a new recipe"""
        # access data from json using request obeject that gets it from the frontend
        data = request.get_json()

        new_recipe=Recipe(
            title=data.get('title'),
            description=data.get('description'),
        )

        new_recipe.save()
        return new_recipe, 201

# recipe model route to add,delete and update recipes
@api.route('/recipe/<int:id>')
class recipeResource(Resource):

    @api.marshal_with(recipe_model)
    def get(self,id):
        """Get a recipe by id"""
        recipe = Recipe.query.get_or_404(id)
        
        return recipe
    
    @api.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe"""
        recipe_to_update=Recipe.query.get_or_404(id)

        data=request.get_json()

        recipe_to_update.update(data.get('title'), data.get('description'))

        return recipe_to_update

    @api.marshal_with(recipe_model)
    @jwt_required()
    def delete(self,id):
        """delete a recipe"""
        recipe_to_delete=Recipe.query.get_or_404(id)

        recipe_to_delete.delete()

        return recipe_to_delete

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "recipe":Recipe
    }

if(__name__) == '__main__':
    app.run()

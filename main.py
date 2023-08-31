from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db

# config the app
app=Flask(__name__)
app.config.from_object(DevConfig)

# register sqlalchemy to work with our app
db.init_app(app)

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

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}

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
    def put(self,id):
        """update a recipe"""
        recipe_to_update=Recipe.query.get_or_404(id)

        data=request.get_json()

        recipe_to_update.update(data.get('title'), data.get('description'))

        return recipe_to_update

    @api.marshal_with(recipe_model)
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

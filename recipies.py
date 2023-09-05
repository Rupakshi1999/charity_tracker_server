from flask_restx import Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from models import Recipe

#create namespace
recipie_namespace=Namespace('recipe', description="A namespace for our recipie table")

# Searilize the database data into json to use on front end
recipe_model=recipie_namespace.model(
    # model {searializer tem[plate]}
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)

@recipie_namespace.route('/recipes')
class RecipesResource(Resource):

    @recipie_namespace.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes from the databse"""
        # Get the recipes in sqlalchemy object
        recipes = Recipe.query.all()

        # convert it into json using serilizer and return
        return recipes

    @recipie_namespace.marshal_with(recipe_model)
    @recipie_namespace.expect(recipe_model)
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
@recipie_namespace.route('/recipe/<int:id>')
class recipeResource(Resource):

    @recipie_namespace.marshal_with(recipe_model)
    def get(self,id):
        """Get a recipe by id"""
        recipe = Recipe.query.get_or_404(id)
        
        return recipe
    
    @recipie_namespace.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe"""
        recipe_to_update=Recipe.query.get_or_404(id)

        data=request.get_json()

        recipe_to_update.update(data.get('title'), data.get('description'))

        return recipe_to_update

    @recipie_namespace.marshal_with(recipe_model)
    @jwt_required()
    def delete(self,id):
        """delete a recipe"""
        recipe_to_delete=Recipe.query.get_or_404(id)

        recipe_to_delete.delete()

        return recipe_to_delete

@recipie_namespace.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}
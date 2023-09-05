from flask_restx import Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from models import Charities

#create namespace
charity_namespace=Namespace('charities', description="A namespace for our charities table")

# Searilize the database data into json to use on front end
charity_model=charity_namespace.model(
    # model {searializer tem[plate]}
    "Charity",
    {
        "id":fields.Integer(),
        "name":fields.String(),
        "short_description":fields.String(),
        "link":fields.String(),
        "img_src":fields.String(),
        "address_line1":fields.String(),
        "city":fields.String(),
        "state":fields.String(),
        "country":fields.String(),
        "zip":fields.Integer()
    }
)

@charity_namespace.route('/charity')
class CharitiesResource(Resource):

    @charity_namespace.marshal_list_with(charity_model)
    def get(self):
        """Get all charities from the databse"""
        # Get the charities in sqlalchemy object
        charities = Charities.query.all()

        # convert it into json using serilizer and return
        return charities

    @charity_namespace.marshal_with(charity_model)
    @charity_namespace.expect(charity_model)
    @jwt_required()
    def post(self):
        """Create a new charity"""
        # access data from json using request obeject that gets it from the frontend
        data = request.get_json()

        new_charities=Charities(
            name=data.get('name'),
            short_description=data.get('short_description'),
            link=data.get('link'),
            img_src=data.get('img_src'),
            address_line1=data.get('address_line1'),
            city=data.get('city'),
            state=data.get('state'),
            country=data.get('country'),
            zip=data.get('zip')
        )

        new_charities.save()
        return new_charities, 201

# charity route to add,delete charity
@charity_namespace.route('/charity/<int:id>')
class recipeResource(Resource):

    @charity_namespace.marshal_with(charity_model)
    def get(self,id):
        """Get a charity by id"""
        charity = Charities.query.get_or_404(id)
        
        return charity

    @charity_namespace.marshal_with(charity_model)
    @jwt_required()
    def delete(self,id):
        """delete a charity"""
        charity_to_delete=Charities.query.get_or_404(id)

        charity_to_delete.delete()

        return charity_to_delete

#  charity route to add,delete charity
@charity_namespace.route('/charity/<string:name>')
class recipeResource(Resource):

    @charity_namespace.marshal_with(charity_model)
    def get(self,name):
        """Get a charity by name"""
        charity = Charities.query.get_or_404(name)
        
        return charity
    
#  charity route 
@charity_namespace.route('/charity/<int:zip>')
class recipeResource(Resource):

    @charity_namespace.marshal_with(charity_model)
    def get(self,zip):
        """Get a charity by zip"""
        charity = Charities.query.get_or_404(zip)
        
        return charity
    
#  charity route
@charity_namespace.route('/charity/<string:state>')
class recipeResource(Resource):

    @charity_namespace.marshal_with(charity_model)
    def get(self,state):
        """Get a charity by state"""
        charity = Charities.query.get_or_404(state)
        
        return charity
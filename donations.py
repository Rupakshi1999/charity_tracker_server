from flask_restx import Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from models import Donation
from datetime import datetime

#create namespace
donation_namespace=Namespace('donation', description="A namespace for our donations table")

# Searilize the database data into json to use on front end
donation_model=donation_namespace.model(
    # model {searializer tem[plate]}
    "Donation",
    {
        "id":fields.Integer(),
        "date":fields.Date(),
        "username":fields.String(),
        "charity_id":fields.Integer(),
        "amount":fields.Float(),
        "motivation":fields.String()
    }
)

@donation_namespace.route('/donation')
class DonationsResource(Resource):

    @donation_namespace.marshal_list_with(donation_model)
    def get(self):
        """Get all donations from the databse"""
        # Get the recipes in sqlalchemy object
        donations = Donation.query.all()

        # convert it into json using serilizer and return
        return donations

    @donation_namespace.marshal_with(donation_model)
    @donation_namespace.expect(donation_model)
    @jwt_required()
    def post(self):
        """Create a new donation"""
        # access data from json using request obeject that gets it from the frontend
        data = request.get_json()

        new_donation=Donation(
            username=data.get('username'),
            charity_id=data.get('charity_id'),
            amount=data.get('amount'),
            date=datetime.now(),
            motivation=data.get('motivation'),
        )

        new_donation.save()
        return new_donation, 201

# recipe donation route to add,delete donation
@donation_namespace.route('/donation/<int:id>')
class recipeResource(Resource):

    @donation_namespace.marshal_with(donation_model)
    def get(self,id):
        """Get a donation by id"""
        donation = Donation.query.get_or_404(id)
        
        return donation

    @donation_namespace.marshal_with(donation_model)
    @jwt_required()
    def delete(self,id):
        """delete a donation"""
        donation_to_delete=Donation.query.get_or_404(id)

        donation_to_delete.delete()

        return donation_to_delete

# recipe donation route
@donation_namespace.route('/donation/<string:username>')
class recipeResource(Resource):

    @donation_namespace.marshal_with(donation_model)
    def get(self,username):
        """Get a donation by username"""
        donation = Donation.query.get_or_404(username)
        
        return donation
    
 # recipe donation route to
@donation_namespace.route('/donation/<int:charity_id>')
class recipeResource(Resource):

    @donation_namespace.marshal_with(donation_model)
    def get(self,charity_id):
        """Get a donation by charity_id"""
        donation = Donation.query.get_or_404(charity_id)
        
        return donation
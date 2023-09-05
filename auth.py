from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

#create namespace
auth_namespace=Namespace('authorization', description="A namespace for our user login and signup")

signup_model=auth_namespace.model(
    # model {searializer tem[plate]}
    "signup",
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model=auth_namespace.model(
    # model name {searializer tem[plate]}
    "login",
    {
        "username":fields.String(),
        "password":fields.String()
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    # show the format of data in /docs post
    @auth_namespace.expect(signup_model)
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


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        login_data=request.get_json()

        username = login_data.get('username')
        password = login_data.get('password')

        db_user= User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
        
        return jsonify({"access_token":access_token, "refresh_token":refresh_token})
    
@auth_namespace.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # access the currect logged in user
        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}), 200)
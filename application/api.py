from application.models import User
from application.validation import NotFoundError
from flask_restful import Resource, marshal_with, fields, reqparse
from .database import db
from  .blacklist import BLACKLIST
from flask import jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import check_password_hash, generate_password_hash

user_output = {"uid": fields.Integer, "user_fname": fields.String, "user_email": fields.String}

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cant be blank"
                        )
    # parser.add_argument('user_lname',
    #                     type=str,
    #                     required=True,
    #                     help="username cant be blank"
    #                     )
    parser.add_argument('user_email',
                        type=str,
                        required=True,
                        help="username cant be blank"
                        )                        
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be blank"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()
        user = db.session.query(User).filter(
            User.user_email == data['user_email']
        )
        if user:
            return {
                "message":"user already exists"
            }
        else:
            hash_ = generate_password_hash(data['password']).decode('utf-8')
            user = User(data['username'], hash_)
            #  save to data base -- need to add
                        

        return {
            "message":"user with id {} added".format(data["username"])
        }
    

class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cant be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be blank"
                        )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = db.session.query(User).filter(User.email == data['username'])
        
        if user:
            print(user.password)
            if check_password_hash(user.password,data['password']):
                access_token = create_access_token(identity= user.username,fresh=True)
                refresh_token = create_refresh_token(user.username)
            
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200
            else:
                return {
                    "message": "wrong password"
                },400
        else:
            return {
                "message": "username not found"
            },400

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message':'Successfully logged out.'},200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {'access_token':new_token},200

class VerifyJWT(Resource):
    @jwt_required()
    def get(self):
        return {"message": "token valid"},200



class UserAPI(Resource):
    @marshal_with(user_output)
    def get(self, username):
        user = db.session.query(User).filter(User.user_fname == username).first()
        print(user)
        
        if user:
           return user
        else:
            print('Enter')
            raise NotFoundError(status_code=404)
    
    def post(self):
        return {}
    
    def put(self, username):
        return {}
    
    def delete(self, username):
        return {}

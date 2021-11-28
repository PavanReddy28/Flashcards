import os
from flask import Flask
from application import config
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_security import Security, SQLAlchemySessionUserDatastore
from datetime import timedelta
from application.config import LocalDevelopmentConfig
from application.database import db
import logging
from application.models import User, Role
from flask_security.forms import RegisterForm, StringField, Required
from application.blacklist import BLACKLIST


app = None
api = None
jwt = None

ACCESS_EXPIRES = timedelta(hours=1)

from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    username = StringField('First Name', [Required()])

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("No Production config setup.")
    else:
        print("Starting Local Development.")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt = JWTManager(app)

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # security = Security(app, user_datastore)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()
    return app, api, jwt


app, api, jwt = create_app()


from application.controllers import *

from application.api import UserAPI, UserRegister, UserLogin

api.add_resource(UserAPI, "/user/<string:username>")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message=False), 404

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return render_template('404.html', message=True), 401

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST 


if __name__ == '__main__':
    app.run(debug=True)

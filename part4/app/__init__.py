from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

import config

from app.api.v1.admin import api as admin_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns



def create_app(config_class=config.DevelopmentConfig):
    """
    Application factory to create and configure the Flask app instance.

    Parameters:
        config_class (str or class): The configuration class or import path
            to use for the Flask application. Defaults to
            'config.DevelopmentConfig'.

    Returns:
        Flask: Configured Flask application instance.

    This factory:
    - Instantiates the Flask app.
    - Loads configuration from the provided config class.
    - Initializes the Flask-RESTx API and registers namespaces.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app

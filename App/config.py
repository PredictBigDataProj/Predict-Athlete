import os
import importlib
from datetime import timedelta
# from App.controllers import load_models

#app, overrides

def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7

    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
    else:
        config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        config['DEBUG'] = config['ENV'].upper() != 'PRODUCTION'
        delta = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 7))


    # if os.path.exists(os.path.join('./App', 'custom_config.py')):
    #     app.config.from_object('App.custom_config')
    # else:
    #     app.config.from_object('App.default_config')

    config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(delta))
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config['TEMPLATES_AUTO_RELOAD'] = True
    config['SEVER_NAME'] = '0.0.0.0'
    config['PREFERRED_URL_SCHEME'] = 'https'
    config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]

    config["JWT_COOKIE_SECURE"] = True
    config["JWT_COOKIE_CSRF_PROTECT"] = False
    config['FLASK_ADMIN_SWATCH'] = 'darkly'
    config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    return config

    # app.config.from_prefixed_env()
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.config['PREFERRED_URL_SCHEME'] = 'https'
    # app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    # app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    # app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    # app.config["JWT_COOKIE_SECURE"] = True
    # app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    # app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

    # models_dict, selected_features_dict, pca_dict, scaler = load_models()

    # app.config['MODELS_DICT'] = models_dict
    # app.config['SELECTED_FEATURES_DICT'] = selected_features_dict
    # app.config['PCA_DICT'] = pca_dict
    # app.config['SCALER'] = scaler

    # for key in overrides:
    #     app.config[key] = overrides[key]
    
config = load_config()
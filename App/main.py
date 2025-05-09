import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context,
    setup_flask_login,
    load_models
)

from App.views import views, setup_admin




def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_flask_login(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()


    @app.before_first_request
    def load_models_once():
        if not hasattr(app, 'models_loaded'):
            models_dict, selected_features_dict, pca_dict, scaler = load_models()
            app.config['MODELS_DICT'] = models_dict
            app.config['SELECTED_FEATURES_DICT'] = selected_features_dict
            app.config['PCA_DICT'] = pca_dict
            app.config['SCALER'] = scaler
            app.models_loaded = True 
            print("Models loaded successfully.")
    return app

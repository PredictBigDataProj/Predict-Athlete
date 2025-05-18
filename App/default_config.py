import os


SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret-key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
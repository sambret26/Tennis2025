import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            print("WARNING: DATABASE_URL is not set in .env file")
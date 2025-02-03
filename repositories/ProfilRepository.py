from models.Profil import Profil
from database import db

class ProfilRepository:

    @staticmethod
    def getAllProfils():
        return Profil.query.all()
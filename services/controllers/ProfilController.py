from flask import Blueprint, jsonify, request
from repositories.ProfilRepository import ProfilRepository

profilRepository = ProfilRepository()

profilBp = Blueprint('profilBp', __name__, url_prefix='/profils')

@profilBp.route('/', methods=['GET'])
def getProfils():    
    profils = profilRepository.getAllProfils()
    return jsonify([profil.toDict() for profil in profils]), 201
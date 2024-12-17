from flask import Blueprint, jsonify, request
from repositories.PaiementRepository import PaiementRepository
from models.Paiement import Paiement

paiementBp = Blueprint('paiementBp', __name__, url_prefix='/paiements')

@paiementBp.route('/', methods=['GET'])
def getPaiements():
    paiements = PaiementRepository.getAllPaiements()
    return jsonify([paiement.toDict() for paiement in paiements]), 200

@paiementBp.route('/', methods=['POST'])
def addPaiement():
    paiement = Paiement.fromJson(request.json)
    PaiementRepository.addPaiement(paiement)
    return jsonify({'message': 'Paiement added successfully!'}), 201

@paiementBp.route('/multiple', methods=['POST'])
def addPaiements():
    paiements = []
    for data in request.json:
        paiements.append(Paiement.fromJson(data))
    PaiementRepository.addPaiements(paiements)
    return jsonify({'message': 'Paiements added successfully!'}), 201